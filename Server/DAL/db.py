from pymongo import MongoClient
from bunnet import init_bunnet
from functools import lru_cache

@lru_cache()
def get_db():    
    print("connecting to DB...")
    client = MongoClient("mongodb+srv://noyaaberjil_db_user:SwLY9W2VAjStssIT@cluster0.zxasbcw.mongodb.net/") 
    print("connected to DB.")
    return client.CockBook


def init_db(document_models: list = None):
    init_bunnet(database=get_db(), document_models=document_models)
