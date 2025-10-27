from pymongo import MongoClient
from bunnet import Document, init_bunnet
from bson import ObjectId
import datetime
import gridfs

class Recipe(Document):
    userName: str  
    recipe: str  
    rate: float
    status: str  
    dop: datetime
    
    def changeStatus(self, newState):
        self.status = newState
        self.save()
    
    def add_file(self,DB,file_data,content_type):
        # TODO: check if the user exits before adding the file
        # TODO: delete old files before if needed
        fs = gridfs.GridFS(DB)
        fs.put(file_data,user_id=str(self.id),contentType=content_type) # can add more custom fields like filename, description ....etc

    def get_file(self,DB):
        fs = gridfs.GridFS(DB)
        data = DB.fs.files.find_one({'user_id':str(self.id)})
        if data == None:
            return None,None
        
        f_id = data['_id']
        output_data = fs.get(f_id).read()
        return output_data,data['contentType']
    

