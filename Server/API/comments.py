from fastapi import APIRouter,Response,status,UploadFile
from DAL.comments import Comments
from datetime import datetime


router = APIRouter(prefix="/Comments")

@router.post("/add")
def add_comment(comment: Comments):
    comment.dop = comment.dop or datetime.now()  
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