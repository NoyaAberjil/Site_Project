from nicegui import ui, app
from requests import get, post
from fastapi import status



def clear_cards(container):
    container.clear()


def update_recipe_cards(container, recipes):
    clear_cards(container)

    for i in range(0, len(recipes), 3):
        with container:
            with ui.row().classes('justify-center gap-4 w-full'):
                for j in range(3):
                    if i + j < len(recipes):
                        recipe = recipes[i + j]
                        with ui.card().classes('w-96 bg-[#ffffff] shadow-md p-4 rounded-xl cursor-pointer'):
                            ui.label(recipe['userName']).classes('text-lg font-bold text-[#4a3c2a] text-center')
                            ui.label(recipe['recipeName']).classes('text-sm text-[#6b5e4a] text-center mb-3')
                            with ui.link(target= "/Recipe/"+recipe['_id']):
                                # ui.image(f"http://127.0.0.1:8090/recipe/file/{recipe['_id']}").classes('w-full object-contain rounded-lg mb-3')
                                ui.image(f"http://127.0.0.1:8090/recipe/file/{recipe['_id']}").classes('w-64')

                            with ui.row().classes('justify-between items-center w-full'):
                                with ui.row().classes('gap-1'):
                                    ui.rating(value=recipe['rate'], size="md", color="yellow").disable()



def load_all_recipes(container):
    response = get("http://127.0.0.1:8090/recipe/approved")
    recipes = response.json() if response.status_code == status.HTTP_200_OK else []
    update_recipe_cards(container, recipes)

def load_user_recipes(container):
    response = get("http://127.0.0.1:8090/recipe/user/"+ app.storage.user.get("user_id"))
    recipes = response.json() if response.status_code == status.HTTP_200_OK else []
    update_recipe_cards(container, recipes)

def load_admin_recipes(container):
    response = get("http://127.0.0.1:8090/recipe/admin?user_id="+ app.storage.user.get("user_id"))
    recipes = response.json() if response.status_code == status.HTTP_200_OK else []
    update_recipe_cards(container, recipes)

def logout():
    app.storage.user.clear()
    ui.navigate.to('/')

def filter_recipes(container, recipe_type, difficulty):
    recipe_type_value = "" if recipe_type == "כל המתכונים" else recipe_type
    difficulty_value = "" if difficulty == "כל המתכונים" else difficulty

    if not recipe_type_value and not difficulty_value:
        load_all_recipes(container)
        return

    data = {"recipeType": recipe_type_value, "difficulty": difficulty_value}
    response = post("http://127.0.0.1:8090/recipe/filter", json=data)
    if response.status_code == status.HTTP_200_OK:
        update_recipe_cards(container, response.json())
    else:
        ui.notify("שגיאה בטעינת המתכונים", color="red")

def load_favorite_recipes(container):
    response = get("http://127.0.0.1:8090/recipe/favorites/"+ app.storage.user.get("user_id"))
    recipes = response.json() if response.status_code == status.HTTP_200_OK else []
    update_recipe_cards(container, recipes)


@ui.page('/PersonalPage', title="PersonalPage", favicon='Images/logo3.jpg')
def PersonalPage_page():

    ui.add_head_html("<div dir=rtl>")
    ui.query('body').classes('bg-[#f4f1ea]')

    drawer = ui.drawer('left', bordered=True).classes('bg-[#f4f1ea] w-48')
    with drawer:
        ui.label('תפריט ראשי').classes('text-lg font-bold mb-4 text-[#4a3c2a]')
        ui.button('בית',on_click=lambda: load_all_recipes(recipes_container)).classes('block mb-2 text-[#4a3c2a]')
        ui.button('פרופיל',on_click=lambda: load_user_recipes(recipes_container)).classes('block mb-2 text-[#4a3c2a]')
        if app.storage.user.get("is_admin"):
            ui.button('מתכונים לאישור',on_click=lambda: load_admin_recipes(recipes_container)).classes('block mb-2 text-[#4a3c2a]')
        ui.button('מועדפים',on_click=lambda: load_favorite_recipes(recipes_container)).classes('block mb-2 text-[#4a3c2a]')
        ui.button('הוספת מתכון', on_click=lambda: (ui.navigate.to('/AddRecipe'))).classes('block mb-2 text-[#4a3c2a]')
        ui.button('התנתקות', on_click=logout).classes('block mb-2 text-[#4a3c2a]')

    with ui.row().classes('w-full bg-[#f0ece1] p-3 items-center shadow-md'):
        with ui.row().classes('flex-1 justify-start'):
            ui.icon('menu').classes('text-2xl cursor-pointer text-[#4a3c2a]').on('click', drawer.toggle)

        with ui.row().classes('flex-1 justify-center'):
            ui.image("Images/logo3.jpg").classes('w-16 h-16 object-contain')

        with ui.row().classes('flex-1'):  
            pass

    # ---------- Filters ----------
    with ui.row().classes('justify-center gap-4 w-full mt-4 mb-6'):
        recipe_type_dropdown = ui.select(
            ['כל המתכונים', 'מתוק', 'מלוח', 'דיאטטי'],
            value='כל המתכונים',
            label='קטגוריה'
        ).classes('w-48')

        difficulty_dropdown = ui.select(
            ['כל המתכונים', 'קל', 'בינוני', 'קשה'],
            value='כל המתכונים',
            label='רמת קושי'
        ).classes('w-48')

        ui.button(
            'חפש',
            on_click=lambda: filter_recipes(
                recipes_container,
                recipe_type_dropdown.value,
                difficulty_dropdown.value
            )
        ).classes('bg-[#e0c9a6] text-[#4a3c2a] rounded-lg px-4 py-2')

    with ui.column().classes('w-full') as recipes_container:
        pass

    load_all_recipes(recipes_container)

