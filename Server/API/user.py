from fastapi import APIRouter,Response,status,UploadFile

from DAL.user import User, UserLogin, AddFavoriteRequest

router = APIRouter(prefix="/user")

# find all users
@router.get("/all")
def api_get_all():
    return User.find().run()


# add user
@router.post("")
def api_add(user: User):
    if User.get(user.id).run() != None:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        new_user = User(
        id=user.id,
        email=user.email,
        password=user.password,
        is_admin=user.is_admin,
        favorites=user.favorites)
        new_user.save()
        return new_user

# update user
@router.put("")
def api_udpate(user: User):
    the_user:User = User.get(user.id).run() 
    if the_user == None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        user.save()
        return user


# delete user
@router.delete("/{userName}")
def api_delete(userName: str):
    the_user:User = User.get(userName).run() 
    if the_user == None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        the_user.delete()
        return Response(status_code=status.HTTP_200_OK)


# find single user
@router.get("/{userName}")
def api_get(userName: str):
    the_user:User = User.get(userName).run() 
    if the_user == None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return the_user


# login
@router.post("/login")
def api_login(ul: UserLogin) :
    the_user:User = User.get(ul.user_name).run() 
    if the_user == None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    elif the_user.password != ul.password:
        return Response(status_code=status.HTTP_404_NOT_FOUND)        
    else:
        return the_user
    
# get favorites
@router.post("/favorites/{userName}")
def api_favorites(userName: str):
    the_user: User = User.get(userName).run()
    if the_user is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return {"favorites": the_user.favorites}

# add favorites
@router.post("/favorites/add")
def add_favorite(req: AddFavoriteRequest):
    the_user: User = User.get(req.user_name).run()

    if the_user is None:
        return Response(content="User not found", status_code=status.HTTP_404_NOT_FOUND)
    
    the_user.addFavorites(req.recipe_id)

    return {
        "message": f"Recipe {req.recipe_id} added to favorites.",
        "favorites": the_user.favorites
    }
    
