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

