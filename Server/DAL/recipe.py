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
    
    def changeStatus(self, newState):
        self.status = newState
        self.save()
    
    def add_file(self,file_data,content_type):
        # TODO: check if the user exits before adding the file
        # TODO: delete old files before if needed
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


    

