from bunnet import Document
# from bson import ObjectId
from datetime import datetime

class Comments(Document):
    Recipe_ID: str
    userName: str
    comment: str  
    dop: datetime
 
    


