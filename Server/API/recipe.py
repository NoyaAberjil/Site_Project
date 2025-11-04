from fastapi import APIRouter,Response,status,UploadFile
from datetime import datetime
from DAL.recipe import Recipe, recipeFilter
from DAL.user import User

router = APIRouter(prefix="/recipe")

# add user
@router.post("")
def api_add(recipe: Recipe):
    if Recipe.find((recipe.userName == User.id)).run():
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        recipe.save()
        return recipe

# filter users
@router.post("/filter")
def api_get_filter(filter:recipeFilter):
    return Recipe.find({'difficulty':filter.difficulty,'recipeType':filter.recipeType}).run()
