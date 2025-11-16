from DAL.recipe import Recipe
from DAL.comments import Comments
from DAL.user import User
from fastapi import FastAPI
import uvicorn
import DAL.db
from API.user import router as user_router
from API.recipe import router as recipe_router
from API.comments import router as comments_router
# from api.task import router as task_router


if __name__ == "__main__":
    uvicorn.run("main:app", port=8090,reload=True)
else:
    DAL.db.init_db([User, Recipe, Comments])
    app = FastAPI()
    app.include_router(user_router)
    app.include_router(recipe_router)
    app.include_router(comments_router)





#example for sort in MDB
# def findUsersByGender(gender):
#     if gender =="":
#         findresult = User.find() # find all documents
#     else:
#         findresult = User.find(User.gender==gender)
#     return findresult.to_list()
#     # for more search options, see: https://roman-right.github.io/bunnet/tutorial/finding-documents/#search-criteria
#     # findresult = User.find(User.age>=12) # simple search
#     # findresult = User.find(User.age>=12).sort(-User.name) # simple search with sort. use '-' or '+'
#     # findresult = User.find(User.age>=12,User.age<15 ).sort(+User.age) # more than one search   
#     # findresult = User.find(User.age>=12).limit(2) # with limit to the number of results