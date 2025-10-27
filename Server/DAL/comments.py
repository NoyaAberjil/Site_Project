from pymongo import MongoClient
from bunnet import Document, init_bunnet
from bson import ObjectId
import datetime

class Comments(Document):
    Recipe_ID: ObjectId
    userName: str
    comment: str  
    dop: datetime
 
    


