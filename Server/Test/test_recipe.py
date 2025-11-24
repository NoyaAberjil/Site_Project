from fastapi import FastAPI,status
from fastapi.testclient import TestClient
from main import app
from  DAL.user import * 
from  DAL.recipe import * 
from  DAL.comments import * 
import random

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



def test_add_recipe():
    user = generate_user(True)
    client.post("/user", json=user.model_dump())

    recipe = generate_recipe(user.id, "easy", "main")

    resp = client.post("/recipe", json=recipe.model_dump(mode="json"))
    assert resp.status_code == 200

    data = resp.json()
    assert data["recipeName"] == recipe.recipeName
    assert data["userName"] == user.id

    client.delete(f"/recipe/{data['_id']}")
    user.delete()

def test_recipe_filter():
    user = generate_user(True)
    client.post("/user", json=user.model_dump())

    recipe1 = generate_recipe(user.id, "קל", "מתוק")       # approved
    recipe1.status = "approved"
    recipe1.save()

    recipe2 = generate_recipe(user.id, "קל", "מתוק")       # approved
    recipe2.status = "approved"
    recipe2.save()

    recipe3 = generate_recipe(user.id, "קל", "מתוק")       # pending
    recipe3.status = "pending"
    recipe3.save()

    recipe4 = generate_recipe(user.id, "קשה", "מלוח")      # approved
    recipe4.status = "approved"
    recipe4.save()

    filter_data = {"difficulty": "קל", "recipeType": "מתוק"}
    response = client.post("/recipe/filter", json=filter_data)
    assert response.status_code == 200

    data = response.json()

    assert all(r["status"] == "approved" and r["difficulty"] == "קל" and r["recipeType"] == "מתוק" for r in data)

    recipe1.delete()
    recipe2.delete()
    recipe3.delete()
    recipe4.delete()
    user.delete()

def test_get_approved_recipes():
    user = generate_user(True)
    client.post("/user", json=user.model_dump())

    approved_recipe = generate_recipe(user.id, "קל", "מתוק")
    approved_recipe.status = "approved"
    approved_recipe.save()

    pending_recipe = generate_recipe(user.id, "קשה", "מלוח")
    pending_recipe.status = "pending"
    pending_recipe.save()

    response = client.get("/recipe/approved")
    assert response.status_code == 200
    data = response.json()
    for recipe in data:
        assert recipe["status"] == "approved"
    
    approved_recipe.delete()
    pending_recipe.delete()
    user.delete()

def test_get_user_recipes():
    user1 = generate_user(True)
    client.post("/user", json=user1.model_dump())

    recipe1 = generate_recipe(user1.id, "קל", "מתוק")
    recipe1.save()
    recipe2 = generate_recipe(user1.id, "קשה", "מלוח")
    recipe2.save()

    user2 = generate_user(True)
    client.post("/user", json=user2.model_dump())

    recipe3 = generate_recipe(user2.id, "בינוני", "דיאטטי")
    recipe3.save()

    response = client.get(f"/recipe/user/{user1.id}")
    assert response.status_code == 200
    data = response.json()
    for recipe in data:
        assert recipe["userName"] == user1.id
        assert recipe["userName"] != user2.id

    
    recipe1.delete()
    recipe2.delete()
    recipe3.delete()
    user1.delete()
    user2.delete()


def test_get_admin_recipes():
    admin_user = generate_user(True)
    client.post("/user", json=admin_user.model_dump())

    normal_user = generate_user(False)
    client.post("/user", json=normal_user.model_dump())

    recipe1 = generate_recipe(admin_user.id, "קל", "מתוק")  # pending
    recipe1.status = "pending"
    recipe1.save()

    recipe2 = generate_recipe(admin_user.id, "בינוני", "דיאטטי")  # approved
    recipe2.status = "approved"
    recipe2.save()

    recipe3 = generate_recipe(normal_user.id, "קשה", "מלוח")  # pending
    recipe3.status = "pending"
    recipe3.save()

    response = client.get(f"/recipe/admin?user_id={admin_user.id}")
    assert response.status_code == 200
    data = response.json()
    
    for recipe in data:
        assert recipe["status"] == "pending"

    recipe1.delete()
    recipe2.delete()
    recipe3.delete()
    admin_user.delete()
    normal_user.delete()


def test_get_admin_recipes():
    admin_user = generate_user(True)
    client.post("/user", json=admin_user.model_dump())

    normal_user = generate_user(False)
    client.post("/user", json=normal_user.model_dump())

    recipe1 = generate_recipe(admin_user.id, "קל", "מתוק")  # pending
    recipe1.status = "pending"
    recipe1.save()

    recipe2 = generate_recipe(admin_user.id, "בינוני", "דיאטטי")  # approved
    recipe2.status = "approved"
    recipe2.save()

    recipe3 = generate_recipe(normal_user.id, "קשה", "מלוח")  # pending
    recipe3.status = "pending"
    recipe3.save()

    response = client.get(f"/recipe/admin?user_id={admin_user.id}")
    assert response.status_code == 200
    data = response.json()
    
    for recipe in data:
        assert recipe["status"] == "pending"

    recipe1.delete()
    recipe2.delete()
    recipe3.delete()
    admin_user.delete()
    normal_user.delete()

def test_delete_recipe():
    user = generate_user(True)
    client.post("/user", json=user.model_dump())

    recipe = generate_recipe(user.id, "קל", "מתוק")
    recipe.save()

    response = client.delete(f"/recipe/{recipe.id}")
    assert response.status_code == 200
    assert Recipe.get(recipe.id).run() is None

    user.delete()   

def test_change_rate():
    # יצירת משתמש ומתקן
    user1 = generate_user(True)
    user2 = generate_user(True)
    user3 = generate_user(True)
    client.post("/user", json=user1.model_dump())
    client.post("/user", json=user2.model_dump())
    client.post("/user", json=user3.model_dump())

    recipe = generate_recipe(user1.id, "קל", "מתוק")
    recipe.save()
    recipe_id = str(recipe.id)

    response = client.post(f"/recipe/rate/{recipe_id}?new_rate=4.0&user_id={user2.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["rate"] == 4.0
    assert user2.id in data["rated_user"]

    response = client.post(f"/recipe/rate/{recipe_id}?new_rate=2.0&user_id={user3.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["rate"] == 3.0
    assert user3.id in data["rated_user"]

    response = client.post(f"/recipe/rate/{recipe_id}?new_rate=5.0&user_id={user2.id}")
    assert response.status_code == 400 

    recipe.delete()
    response = client.post(f"/recipe/rate/{recipe_id}?new_rate=5.0&user_id={user2.id}")
    assert response.status_code == 404

    user1.delete()
    user2.delete()
    user3.delete()
 










