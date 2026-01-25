from nicegui import ui, app
from datetime import datetime
from requests import get, post
from PersonalPage import load_all_recipes, load_user_recipes, load_admin_recipes

def logout():
    app.storage.user.clear()
    ui.navigate.to('/')

@ui.page('/Recipe/{recipe_id}',title="Recipe",favicon='Images/logo3.jpg')
def Recipe_page(recipe_id : str):
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
            if app.storage.user.get("is_admin"):
                with ui.row().classes('justify-center gap-4 mb-4'):
                    ui.button('אישור', color='green', icon='check').classes('px-4 py-2 text-white rounded-lg shadow-md')
                    ui.button('דחייה', color='red', icon='close').classes('px-4 py-2 text-white rounded-lg shadow-md')
                    
            response = get(f"http://127.0.0.1:8090/recipe/id/{recipe_id}")
            recipe = response.json()

            with ui.row().classes('items-center justify-between w-full'):
                with ui.row().classes('gap-1'):
                    ui.rating(value=0, size="md").classes('material-icons text-yellow-500 cursor-pointer')

                ui.image(f"http://127.0.0.1:8090/recipe/file/{recipe['_id']}").classes(
                    'w-64 h-48 object-cover rounded-lg'
                )

                ui.chip(selectable=True, icon='bookmark', color='orange').classes(
                    'material-icons text-orange-500 cursor-pointer'
                )
            
                with ui.column().classes('gap-1'):
                    ui.label(f"קטגוריה: {recipe['recipeType']}").classes('text-md font-semibold text-[#4a3c2a]')
                    ui.label(f"רמת קושי: {recipe['difficulty']}").classes('text-md font-semibold text-[#4a3c2a]')

            
            
            ui.label(str(recipe['recipeName'])).classes('text-xl font-bold text-[#4a3c2a] text-center mt-4')

            ui.label('מצרכים:').classes('text-lg font-semibold text-[#4a3c2a] mt-4 mb-2')
            ingredients = recipe['ingredients']
            with ui.column().classes('gap-2'):
                for item in ingredients:
                    ui.checkbox(item)

            ui.label('הוראות הכנה:').classes('text-lg font-semibold text-[#4a3c2a] mt-6 mb-2')
            instructions = recipe['recipe']
            ui.label(instructions).classes('text-sm text-[#6b5e4a] whitespace-pre-line')
            

        ui.label('תגובות').classes('text-xl font-bold text-[#4a3c2a] mt-8 mb-4')

        comments_column = ui.column().classes('w-[600px] gap-4')
        
        # שם משתמש קבוע בקוד
        username = recipe['userName']

        def add_comment():
            text = comment_input.value.strip()
            if text:
                timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")  # פורמט תאריך ושעה
                with comments_column:
                    with ui.card().classes('w-full bg-[#faf7f2] p-3 rounded-lg shadow-sm'):
                        ui.label(f"{username} · {timestamp}").classes('text-sm font-bold text-[#4a3c2a]')
                        ui.label(text).classes('text-sm text-[#6b5e4a]')
                comment_input.value = ''

        # שדה תגובה בלבד
        with ui.row().classes('w-[600px] gap-2 mt-2'):
            comment_input = ui.input(placeholder='הוסף תגובה...').classes('flex-1')
            ui.button('שלח', on_click=add_comment).classes(
                'bg-[#4a3c2a] text-white rounded-lg px-4 py-2'
            )


