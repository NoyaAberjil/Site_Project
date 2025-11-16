from pymongo import MongoClient
from bunnet import Document, init_bunnet
from pydantic import BaseModel

class UserLogin(BaseModel):
    user_name: str
    password: str

class AddFavoriteRequest(BaseModel):
    user_name: str
    recipe_id: str

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

