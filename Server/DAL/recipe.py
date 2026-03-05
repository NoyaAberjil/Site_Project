from pymongo import MongoClient
from bunnet import Document, init_bunnet
from datetime import datetime
import gridfs
from DAL.db import get_db
from pydantic import BaseModel

class recipeFilter(BaseModel):
    difficulty: str
    recipeType: str
    
class recipeRating(BaseModel):
    new_rate: float
    user_id: str
    recipe_id: str

class recipeStatus(BaseModel):
    recipe_id: str
    status: str

   
class Recipe(Document):
    userName: str  
    recipe: str  
    recipeName: str
    ingredients: list[str]
    rate: float
    rated_user: list[str]
    status: str  
    difficulty : str
    recipeType: str
    dop: datetime
    def validate_recipe(self) -> tuple[bool, str]:
        """ולידציה של נתוני המתכון לפני שמירה"""
        
        VALID_DIFFICULTIES = ['קל', 'בינוני', 'קשה']
        VALID_TYPES = ['מתוק', 'מלוח', 'דיאטטי']

        if not self.recipeName or len(self.recipeName) < 2:
            return False, "שם המתכון חייב להכיל לפחות 2 תווים"
        
        if self.difficulty not in VALID_DIFFICULTIES:
            return False, f"רמת קושי לא תקינה. בחר מבין: {', '.join(VALID_DIFFICULTIES)}"
        
        if self.recipeType not in VALID_TYPES:
            return False, f"סוג מתכון לא תקין. בחר מבין: {', '.join(VALID_TYPES)}"
        
        if not self.ingredients or len(self.ingredients) < 1:
            return False, "חובה להוסיף לפחות מצרך אחד"
        
        if len(self.recipe) < 0:
            return False, "הוראות ההכנה קצרות מדי"
            
        return True, ""
    
    
    def changeStatus(self, newState):
        self.status = newState
        self.save()
    
    def add_file(self,file_data,content_type):
        fs = gridfs.GridFS(get_db())
        fs.put(file_data,recipe_id=str(self.id),contentType=content_type)

    def get_file(self):
        fs = gridfs.GridFS(get_db())
        data = get_db().fs.files.find_one({'recipe_id':str(self.id)})
        if data == None:
            return None,None
        
        f_id = data['_id']
        output_data = fs.get(f_id).read()
        return output_data,data['contentType']


    

