from pymongo import MongoClient
from bunnet import Document, init_bunnet
from pydantic import BaseModel

class UserLogin(BaseModel):
    user_name: str
    password: str

class User(Document):
    id: str
    email: str  
    password: str
    is_admin: bool
    favorites: list[str]
    
    def addFavorites(self, newRecipe):
        if newRecipe not in self.favorites:
            self.favorites.append(newRecipe)
            self.save()



def connect2DB():
    client = MongoClient("mongodb+srv://raz:raz@cluster0.mzxtq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0") #dont forget to changr to my user
    init_bunnet(database=client.home_tasks, document_models=[User])    

# print("start")
# connect2DB()
# # addManyUsers()
# new_user = User(id="NoyaAberjil", email="NoyaAberjil@gmail.com", password="Noya1234")
# new_user.save()

# my_user = User.get("Michael4@gmail.com").run()
# print(my_user)
# my_user.delete()

# print("end")