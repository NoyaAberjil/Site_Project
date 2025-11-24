from fastapi import FastAPI,status
from fastapi.testclient import TestClient
from main import app
from  DAL.user import * 
from  DAL.recipe import * 
from  DAL.comments import * 
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

def test_add_comment():
    owner = generate_user(True)
    client.post("/user", json=owner.model_dump())

    commenter = generate_user(True)
    client.post("/user", json=commenter.model_dump())

    recipe = generate_recipe(owner.id, "easy", "main")
    resp_recipe = client.post("/recipe", json=recipe.model_dump(mode="json"))
    recipe_id = resp_recipe.json()["_id"]

    created_comment_ids = []

    comment_data = {
        "Recipe_ID": recipe_id,
        "userName": commenter.id,
        "comment": "Great dish!",
        "dop": datetime.now().isoformat()
    }

    response = client.post("/Comments/add", json=comment_data)
    assert response.status_code == 200

    new_comment = response.json()
    created_comment_ids.append(new_comment["_id"])

    assert new_comment["comment"] == "Great dish!"
    assert new_comment["Recipe_ID"] == recipe_id
    assert new_comment["userName"] == commenter.id

    commenter.delete()
    commenter_id = commenter.id
    comment_data["Recipe_ID"] = recipe_id
    comment_data["userName"] = commenter_id
    response = client.post("/Comments/add", json=comment_data)
    assert response.status_code == 404
    assert "User not found" in response.text

    client.delete(f"/recipe/{recipe_id}")

    comment_data["Recipe_ID"] = recipe_id
    comment_data["userName"] = owner.id
    response = client.post("/Comments/add", json=comment_data)
    assert response.status_code == 404
    assert "Recipe not found" in response.text

    for cid in created_comment_ids:
        client.delete(f"/Comments/delete/{cid}")

    owner.delete()

def test_delete_comment():
    user = generate_user(True)
    client.post("/user", json=user.model_dump())

    recipe = generate_recipe(user.id, "easy", "main")
    resp_recipe = client.post("/recipe", json=recipe.model_dump(mode="json"))
    recipe_id = resp_recipe.json()["_id"]

    comment_data = {
        "Recipe_ID": recipe_id,
        "userName": user.id,
        "comment": "Nice recipe!",
        "dop": datetime.now().isoformat()
    }

    resp = client.post("/Comments/add", json=comment_data)
    assert resp.status_code == 200
    comment_id = resp.json()["_id"]

    del_resp = client.delete(f"/Comments/delete/{comment_id}")
    assert del_resp.status_code == 200
    assert "Comment deleted successfully" in del_resp.text

    del_resp2 = client.delete(f"/Comments/delete/{comment_id}")
    assert del_resp2.status_code == 404
    assert "Comment not found" in del_resp2.text

    client.delete(f"/recipe/{recipe_id}")
    user.delete()


def test_get_all_comments():
    user = generate_user(True)
    client.post("/user", json=user.model_dump())

    recipe = generate_recipe(user.id, "easy", "main")
    resp_recipe = client.post("/recipe", json=recipe.model_dump(mode="json"))
    recipe_id = resp_recipe.json()["_id"]

    ids = []
    for msg in ["A", "B"]:
        comment_data = {
            "Recipe_ID": recipe_id,
            "userName": user.id,
            "comment": msg,
            "dop": datetime.now().isoformat()
        }
        resp = client.post("/Comments/add", json=comment_data)
        ids.append(resp.json()["_id"])

    resp_all = client.get("/Comments/all")
    assert resp_all.status_code == 200
    all_comments = resp_all.json()

    assert any(c["_id"] == ids[0] for c in all_comments)
    assert any(c["_id"] == ids[1] for c in all_comments)

    for cid in ids:
        client.delete(f"/Comments/delete/{cid}")
    client.delete(f"/recipe/{recipe_id}")
    user.delete()

def test_get_comments_by_recipe():
    user = generate_user(True)
    client.post("/user", json=user.model_dump())

    recipe1 = generate_recipe(user.id, "easy", "main")
    resp1 = client.post("/recipe", json=recipe1.model_dump(mode="json"))
    recipe1_id = resp1.json()["_id"]

    recipe2 = generate_recipe(user.id, "hard", "dessert")
    resp2 = client.post("/recipe", json=recipe2.model_dump(mode="json"))
    recipe2_id = resp2.json()["_id"]

    comment_data = {
        "Recipe_ID": recipe1_id,
        "userName": user.id,
        "comment": "Nice!",
        "dop": datetime.now().isoformat()
    }
    resp_c = client.post("/Comments/add", json=comment_data)
    cid = resp_c.json()["_id"]

    resp_one = client.get(f"/Comments/recipe/{recipe1_id}")
    assert resp_one.status_code == 200
    assert len(resp_one.json()) == 1
    assert resp_one.json()[0]["_id"] == cid

    resp_two = client.get(f"/Comments/recipe/{recipe2_id}")
    assert resp_two.status_code == 200
    assert resp_two.json() == []

    resp_none = client.get("/Comments/recipe/UNKNOWN")
    assert resp_none.status_code == 200
    assert resp_none.json() == []

    client.delete(f"/Comments/delete/{cid}")
    client.delete(f"/recipe/{recipe1_id}")
    client.delete(f"/recipe/{recipe2_id}")
    user.delete()
