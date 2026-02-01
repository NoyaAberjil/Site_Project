from fastapi import APIRouter,Response,status,UploadFile
from datetime import datetime
# from DAL.recipe import Recipe, recipeFilter
from DAL.user import User
from DAL.recipe import Recipe,recipeFilter
from bson import ObjectId

router = APIRouter(prefix="/recipe")

# add recipe
@router.post("")
def api_add(recipe: Recipe):
    recipe.save()
    return recipe

# filter recipes
@router.post("/filter")
def api_get_filter(filter: recipeFilter):
    query = {"status": "approved"}
    if filter.difficulty != "":
        query["difficulty"] = filter.difficulty

    if filter.recipeType != "":
        query["recipeType"] = filter.recipeType

    return Recipe.find(query).run()
    # return Recipe.find({
    #     "difficulty": filter.difficulty,
    #     "recipeType": filter.recipeType,
    #     "status": "approved"
    # }).run()


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

# get recipe
@router.get("/id/{recipe_id}")
def api_get_recipe(recipe_id: str):
    return Recipe.get(recipe_id).run()

#get favorite recipes
@router.get("/favorites/{user_id}")
def api_get_favorite_recipes(user_id: str):
    user = User.get(user_id).run()
    if not user:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    ids = [ObjectId(x) for x in user.favorites]
    return Recipe.find({"_id": {"$in": ids}}).run()

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

# add file for recipe
@router.put("/file/{recipe_id}")
def api_add_file(recipe_id: str,file: UploadFile):
    the_recipe:Recipe = Recipe.get(recipe_id).run() 
    if the_recipe == None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    the_recipe.add_file(file.file,file.content_type)

# get a file for recipe
@router.get("/file/{recipe_id}")
def api_get_file(recipe_id: str):
    the_recipe:Recipe = Recipe.get(recipe_id).run() 
    if the_recipe == None:
        return Response("invalid recipe",status_code=status.HTTP_404_NOT_FOUND)

    f_data,media_type = the_recipe.get_file()
    print(media_type)
    if f_data == None:
        return Response("no file for recipe",status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(content=f_data, media_type=media_type)

@router.delete("/{recipe_id}")
def api_delete_recipe(recipe_id: str):
    recipe = Recipe.get(recipe_id).run()
    if not recipe:
        return Response(status_code=404, detail="Recipe not found")

    recipe.delete()
    return {"status": "Recipe deleted successfully"}