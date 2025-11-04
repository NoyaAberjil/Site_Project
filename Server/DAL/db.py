from pymongo import MongoClient
from bunnet import init_bunnet
from functools import lru_cache

@lru_cache()
def get_db():    
    print("connecting to DB...")
    client = MongoClient("mongodb+srv://noya:aberjil@cluster0.zm00wso.mongodb.net/?appName=Cluster0") 
    print("connected to DB.")
    return client.CockBook


def init_db(document_models: list = None):
    init_bunnet(database=get_db(), document_models=document_models)
