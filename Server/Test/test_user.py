from fastapi import FastAPI,status
from fastapi.testclient import TestClient
from main import app
from  DAL.user import * 
from  DAL.recipe import * 
import random
from pydantic import TypeAdapter

client = TestClient(app)

# generates a new random user
def generate_user(admin)->User:
    user_id = 'test_'+str(random.randint(1, 1000))
    password = 'pass_'+str(random.randint(1, 1000))
    email = 'email_'+str(random.randint(1, 1000))+'@gmail.com'
    new_user:User = User(id=user_id,password=password,email=email,is_admin=admin, favorites=[])
    return new_user


def generate_recipe(user_name: str, difficulty: str, recipeType: str) -> Recipe:
    suffix = str(random.randint(1000, 9999))

    return Recipe(
        userName=user_name,
        recipe=f"מתכון לדוגמה {suffix}",
        recipeName=f"שם מתכון {suffix}",
        ingredients=[f"מרכיב{suffix}", f"עוד מרכיב{suffix}"],
        rate=0,
        rated_user=[],
        status="pending",
        difficulty=difficulty,
        recipeType=recipeType,
        dop=datetime.now()
    )

def test_add():
    new_user:User = generate_user(True)
    response = client.post("/user",data=new_user.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['_id'] == new_user.id
    assert response.json()['password'] == new_user.password
    assert response.json()['email'] == new_user.email

    # try to add the same user again, should get 400
    response = client.post("/user",data=new_user.model_dump_json())
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    new_user.delete()

def test_delete():
    new_user:User = generate_user(True)
    response = client.post("/user",data=new_user.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['_id'] == new_user.id
    assert response.json()['password'] == new_user.password
    assert response.json()['email'] == new_user.email

    user_name = new_user.id
    response = client.delete("/user/"+str(user_name))
    assert response.status_code == status.HTTP_200_OK

    response = client.get("/user/"+str(user_name))
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_all():
    # find how many users are there
    response = client.get("/user/all")
    assert response.status_code == status.HTTP_200_OK
    count = len(response.json())

    # add a new user
    new_user:User = generate_user(True)
    response = client.post("/user",data=new_user.model_dump_json())
    assert response.status_code == status.HTTP_200_OK

    # make sure one user was added to the all response
    response = client.get("/user/all")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == count+1

    new_user.delete()

def test_get_user():
    new_user:User = generate_user(True)
    response = client.post("/user",data=new_user.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['_id'] == new_user.id
    assert response.json()['password'] == new_user.password
    assert response.json()['email'] == new_user.email

    user_name = new_user.id
    response = client.get("/user/"+str(user_name))
    assert response.status_code == status.HTTP_200_OK

    new_user.delete()
    response = client.get("/user/"+str(user_name))
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_login():
    new_user: User = generate_user(True)
    client.post("/user", data=new_user.model_dump_json())

    response = client.post("/user/login", json={
        "user_name": new_user.id,
        "password": new_user.password
    })

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['_id'] == new_user.id

    response = client.post("/user/login", json={
        "user_name": new_user.id,
        "password": "WRONG_PASS"
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND

    new_user.delete()
    response = client.post("/user/login", json={
        "user_name": new_user.id,
        "password": new_user.password
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_recipe_favorites():
    user1 = generate_user(True)
    user2 = generate_user(True)

    client.post("/user", json=user1.model_dump())
    client.post("/user", json=user2.model_dump())

    recipe1 = generate_recipe(user1.id, "easy", "main")
    recipe2 = generate_recipe(user2.id, "medium", "dessert")

    recipe1_dict = recipe1.model_dump(mode="json")
    recipe2_dict = recipe2.model_dump(mode="json")

    resp1 = client.post("/recipe", json=recipe1_dict)
    resp2 = client.post("/recipe", json=recipe2_dict)
    print(resp1)
    print(resp2)

    recipe1_id = resp1.json()['_id']
    recipe2_id = resp2.json()['_id']

    response = client.post("/user/favorites/add", json={"user_name": user1.id, "recipe_id": recipe1_id})
    assert response.status_code == 200
    response = client.post("/user/favorites/add", json={"user_name": user1.id, "recipe_id": recipe2_id})
    assert response.status_code == 200
    favorites = response.json()['favorites']
    assert recipe1_id in favorites
    assert recipe2_id in favorites

    response = client.post("/user/favorites/remove", json={"user_name": user1.id, "recipe_id": recipe1_id})
    assert response.status_code == 200
    favorites = response.json()['favorites']
    assert recipe1_id not in favorites
    assert recipe2_id in favorites

    print("recipe1_id:", recipe1_id)
    print("all recipes:", [r['_id'] for r in client.get("/recipe").json()])
    response = client.delete(f"/recipe/{recipe1_id}")
    assert response.status_code == 200

    response = client.post("/user/favorites/add", json={"user_name": user1.id, "recipe_id": recipe1_id})
    assert response.status_code == 404

    user1.delete()
    user2.delete()
    client.delete(f"/recipe/{recipe2_id}")


def test_get_user_favorites():
    user1 = generate_user(True)
    user2 = generate_user(True)

    client.post("/user", json=user1.model_dump())
    client.post("/user", json=user2.model_dump())

    recipe1 = generate_recipe(user1.id, "easy", "main")
    recipe2 = generate_recipe(user2.id, "medium", "dessert")

    resp1 = client.post("/recipe", json=recipe1.model_dump(mode="json"))
    resp2 = client.post("/recipe", json=recipe2.model_dump(mode="json"))

    recipe1_id = resp1.json()["_id"]
    recipe2_id = resp2.json()["_id"]

    client.post("/user/favorites/add", json={"user_name": user1.id, "recipe_id": recipe1_id})
    client.post("/user/favorites/add", json={"user_name": user1.id, "recipe_id": recipe2_id})

    response = client.get(f"/user/favorites/{user1.id}")
    assert response.status_code == 200
    favorites = response.json()["favorites"]
    assert recipe1_id in favorites
    assert recipe2_id in favorites

    user2_id = user2.id
    user2.delete()
    client.delete(f"/recipe/{recipe2_id}")
    response = client.get(f"/user/favorites/{user2_id}")
    assert response.status_code == 404

    user1.delete()
    client.delete(f"/recipe/{recipe1_id}")


