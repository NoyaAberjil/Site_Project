from fastapi import APIRouter,Response,status,UploadFile
from fastapi.responses import JSONResponse
from DAL.comments import Comments
from datetime import datetime
from DAL.recipe import Recipe,recipeFilter
from DAL.user import User, UserLogin, AddFavoriteRequest

router = APIRouter(prefix="/Comments")

@router.post("/add")
def add_comment(comment: Comments):
    recipe = Recipe.get(comment.Recipe_ID).run()
    recipe = Recipe.get(comment.Recipe_ID).run()
    if recipe is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": "המתכון לא נמצא"}) 
    
    user = User.get(comment.userName).run()
    if user is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": "משתמש לא קיים"})
    
    is_valid, error_message = comment.validate_comment()
    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": error_message})

    comment.dop = comment.dop 

    comment.save()
    return comment


@router.delete("/delete/{comment_id}")
def delete_comment(comment_id: str):
    comment = Comments.get(comment_id).run()
    if not comment:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="Comment not found")
    
    comment.delete()
    return Response(status_code=status.HTTP_200_OK, content="Comment deleted successfully")

@router.get("/all")
def get_all_comments():
    return Comments.find().run()

@router.get("/recipe/{recipe_id}")
def get_comments_by_recipe(recipe_id: str):
    return Comments.find({"Recipe_ID": recipe_id}).run()

