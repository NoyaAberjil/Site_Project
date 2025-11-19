from fastapi import FastAPI,status
from fastapi.testclient import TestClient
from main import app
from  DAL.user import * 
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








# def test_get_filter():
#     # add a new Male admin user 
#     new_user1:User = generate_user("M",True)
#     response = client.post("/user",data=new_user1.model_dump_json())
#     assert response.status_code == status.HTTP_200_OK
#     # add a new FeMale admin user 
#     new_user2:User = generate_user("F",True)
#     response = client.post("/user",data=new_user2.model_dump_json())
#     assert response.status_code == status.HTTP_200_OK
#     # add a new Male not admin user 
#     new_user3:User = generate_user("M",False)
#     response = client.post("/user",data=new_user3.model_dump_json())
#     assert response.status_code == status.HTTP_200_OK
#     # add a new Female not admin user 
#     new_user4:User = generate_user("F",False)
#     response = client.post("/user",data=new_user4.model_dump_json())
#     assert response.status_code == status.HTTP_200_OK

#     # check Male Admin filter
#     uf:UserFilter = UserFilter(gender="M",admin=True)
#     response = client.post("/user/filter",data=uf.model_dump_json())
#     assert response.status_code == status.HTTP_200_OK
#     assert len(response.json()) > 0
#     for d in response.json():
#         assert d["gender"] == "M"
#         assert d["admin"] == True

#     # TODO: check other filter options


#     new_user1.delete()
#     new_user2.delete()
#     new_user3.delete()
#     new_user4.delete()