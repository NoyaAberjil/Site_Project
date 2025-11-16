from fastapi import APIRouter,Response,status,UploadFile
from datetime import datetime
from DAL.recipe import Recipe, recipeFilter
from DAL.user import User

router = APIRouter(prefix="/recipe")

# add recipe
@router.post("")
def api_add(recipe: Recipe):
    recipe.save()
    return recipe

# filter recipes
@router.post("/filter")
def api_get_filter(filter:recipeFilter):
    return Recipe.find({'difficulty':filter.difficulty,'recipeType':filter.recipeType}).run()

#get approved recipes
@router.get("/approved")
def api_get_approved_recipes():
    return Recipe.find({"status": "approved"}).run()

# get recipes
@router.get("")
def api_get_user_recipes():
    return Recipe.find().run()

# get user recipes
@router.get("/user/{user_name}")
def api_get_user_recipes(user_name: str):
    return Recipe.find({"userName": user_name}).run()

# get admin recipes
@router.get("/admin")
def api_get_admin_recipes(user_id: str):
    user = User.get(user_id).run()
    if not user:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


    if not user.is_admin:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    return Recipe.find({"status": "pending"}).run()

# change rate
@router.post("/rate/{recipe_id}")
def api_change_rate(recipe_id: str, new_rate: float, user_id: str):
    recipe = Recipe.get(recipe_id).run()

    if recipe is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    if user_id in recipe.rated_user:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    current_count = len(recipe.rated_user)
    recipe.rate = (recipe.rate * current_count + new_rate) / (current_count + 1)

    recipe.rated_user.append(user_id)

    recipe.save()
    return recipe