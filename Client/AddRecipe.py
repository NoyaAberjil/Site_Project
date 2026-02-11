from nicegui import ui, app
from datetime import datetime
from requests import get, post, put
from threading import Thread 
from asyncio import sleep
import httpx
from fastapi import status


file_data = None

def logout():
    app.storage.user.clear()
    ui.navigate.to('/')

def update_file(event):
    global file_data
    file_data = event.file

async def upload_file(recipe_id):
    file_name = file_data.name
    file_content = await file_data.read()  # Reads the content as bytes
    content_type = file_data.content_type
    
    put('http://127.0.0.1:8090/recipe/file/'+recipe_id,
        files = {"file": (file_name , file_content, content_type)})

async def on_add_recipe_click(recipe_name_input, recipe, ing, category_dropdown, difficulty_dropdown, file_input):
    recipe_data = {
    "userName": app.storage.user.get("user_id"),  
    "recipe":  recipe ,
    "recipeName": recipe_name_input,
    "ingredients": ing.split(","),
    "rate": 0.0,
    "rated_user": [],
    "status": 'pending', 
    "difficulty" : difficulty_dropdown,
    "recipeType": category_dropdown,
    "dop": datetime.now().isoformat()
    }
    response = post('http://127.0.0.1:8090/recipe', json=recipe_data)
    response_data = response.json()
    recipe_id = response_data.get('_id')
    if response.status_code == status.HTTP_200_OK:
        ui.notify('updates saved')
        # add the profile image for the user
        if file_data != None:
            ui.notify('please wait while uploading the file...')
            await upload_file(recipe_id)
            ui.notify("המתכון נוסף בהצלחה!", color="green")
            ui.navigate.to('/PersonalPage')           
    else:
        ui.notify('invalid data')



    ui.notify("המתכון נוסף בהצלחה!", color="green")
    ui.navigate.to('/PersonalPage')


@ui.page('/AddRecipe', title="AddRecipe", favicon='Images/logo3.jpg')
def Recipe_page():
    ui.add_head_html("<div dir=rtl>")
    ui.query('body').classes('bg-[#f4f1ea]')

    drawer = ui.drawer('left', bordered=True).classes('bg-[#f4f1ea] w-48')
    with drawer:
        ui.label('תפריט ראשי').classes('text-lg font-bold mb-4 text-[#4a3c2a]')
        ui.button('בית', on_click=lambda: (ui.navigate.to('/PersonalPage'))).classes('block mb-2 text-[#4a3c2a]')
        ui.button('התנתקות', on_click=logout).classes('block mb-2 text-[#4a3c2a]')

    with ui.row().classes('w-full bg-[#f0ece1] p-3 items-center shadow-md'):
        with ui.row().classes('flex-1 justify-start'):
            ui.icon('menu').classes('text-2xl cursor-pointer text-[#4a3c2a]').on('click', drawer.toggle)
        with ui.row().classes('flex-1 justify-center'):
            ui.image("Images/logo3.jpg").classes('w-16 h-16 object-contain')
        with ui.row().classes('flex-1'):
            pass

    with ui.column().classes('items-center w-full mt-8'):
        with ui.card().classes('w-[600px] bg-white shadow-md rounded-xl p-6'):

            with ui.row().classes('items-center justify-between w-full'):
                file = ui.upload(label="Recipe image",on_upload=lambda e: update_file(e), auto_upload=True,max_files=1).classes('max-w-full')####################3

                with ui.column().classes('gap-2'):
                    category_dropdown = ui.select(
                        ['מתוק', 'מלוח', 'דיאטטי'],
                        value='מתוק',
                        label='קטגוריה'
                    ).classes('w-48')
                    difficulty_dropdown = ui.select(
                        ['קל', 'בינוני', 'קשה'],
                        value='קל',
                        label='רמת קושי'
                    ).classes('w-48')

            # שם המתכון
            recipe_name_input = ui.input(label='שם המתכון',placeholder='כתוב כאן את שם המתכון...').classes('w-full text-center text-xl font-bold text-[#4a3c2a] mt-4')

            # === תיבת טקסט למצרכים ===
            ing =  ui.textarea(
                label='מצרכים',
                placeholder='כתוב כאן את רשימת המצרכים, פסיק אחרי כל מצרך...'
            ).classes('w-full').props('rows=6 mt-2')

            # === תיבת טקסט להוראות הכנה ===
            recipe_input = ui.textarea(
                label='הוראות הכנה',
                placeholder='כתוב כאן את שלבי ההכנה...'
            ).classes('w-full mt-4').props('rows=8')

        # שם משתמש קבוע בקוד
            
        ui.button('העלה', color='#4a3c2a', on_click= lambda:  on_add_recipe_click(recipe_name_input.value, recipe_input.value, ing.value, category_dropdown.value, difficulty_dropdown.value, file) ).classes('mt-6 px-6 py-2 text-white rounded-lg shadow-md')


