from pymongo import MongoClient
from bunnet import Document, init_bunnet
from pydantic import BaseModel
import re
from yagmail import SMTP



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
    
    def validate_user(self) -> tuple[bool, str]:
        if len(self.id) < 2:
            return False, "שם משתמש חייב להיות לפחות 2 תווים"
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.email):
            return False, "פורמט האימייל אינו תקין"
        
        if len(self.password) < 4:
            return False, "הסיסמה חייבת להכיל לפחות 4 תווים"
        
            
        return True, ""

    def addFavorites(self, newRecipe):
        if newRecipe not in self.favorites:
            self.favorites.append(newRecipe)
            self.save()

