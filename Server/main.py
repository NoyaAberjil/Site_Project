from DAL.recipe import Recipe
from DAL.comments import Comments
from  DAL.user import User
from bunnet import init_bunnet
from pymongo import MongoClient
from datetime import datetime 


def connect2db():
    print("connecting to DB...")
    client = MongoClient("mongodb+srv://raz:raz@cluster0.mzxtq.mongodb.net/") #change to my account
    init_bunnet(database=client.HT_3, document_models=[User,Recipe,Comments])
    print("connected to DB.")
    return client.HT_3

def deleteUser(id):
    my_user = User.get(id).run()
    print(my_user)
    my_user.delete()

def addRecipe(name, recipe):
    new_recipe = Recipe(userName=name, recipe=recipe, rate=0.0, status="waiting", dop=datetime.datetime.now())
    new_recipe.save()

def addUser(id, email, password, is_admin=False, favorites=[]):
    new_user = User(id, email, password, is_admin, favorites)
    new_user.save()

def addcomments(name, recipe_id, comment):
    new_comment = Comments(userName=name, Recipe_ID=recipe_id, comment= comment, dop=datetime.datetime.now())
    new_comment.save()


if __name__ == "__main__":
    # Connect to the database
    db = connect2db()

    print("\n--- Testing functions ---")

    # 1️⃣ Test addUser
    print("\n>>> Adding a new user...")
    addUser(id="12345", email="testuser@example.com", password="1234")
    print("User added successfully.")

    # 2️⃣ Test addRecipe
    print("\n>>> Adding a new recipe...")
    addRecipe(name="testuser", recipe="Delicious chocolate cake 🍫")
    print("Recipe added successfully.")

    # 3️⃣ Test addcomments
    print("\n>>> Adding a comment to the recipe...")
    recipe = Recipe.find_one().run()
    if recipe:
        addcomments(name="testuser", recipe_id=recipe.id, comment="Looks really tasty 😋")
        print("Comment added successfully.")
    else:
        print("No recipe found to add a comment to.")

    # 4️⃣ Upload and download a photo for the recipe
    print("\n>>> Uploading a photo for the recipe...")
    if recipe:
        try:
            with open("test_photo.jpg", "rb") as file:
                file_data = file.read()
                recipe.add_file(db, file_data, content_type="image/jpeg")
            print("Photo uploaded successfully.")

            # Download the photo back
            file_data, content_type = recipe.get_file(db)
            if file_data:
                with open("downloaded_photo.jpg", "wb") as output:
                    output.write(file_data)
                print(f"Photo downloaded successfully as 'downloaded_photo.jpg' ({content_type})")
            else:
                print("No photo found for this recipe.")
        except FileNotFoundError:
            print("⚠️ test_photo.jpg not found — please place an image file with that name in the same folder.")
    else:
        print("Skipping photo upload: no recipe found.")

    # 5️⃣ List all users
    print("\n>>> Listing all users:")
    users = User.find_all().run()
    for u in users:
        print(f"- {u.email} (id={u.id})")

    # 6️⃣ Test deleteUser
    print("\n>>> Deleting the test user...")
    deleteUser("12345")
    print("User deleted successfully.")

    print("\n--- Test completed ---")






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