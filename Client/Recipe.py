from nicegui import ui, app
from datetime import datetime
from requests import get, post
from fastapi import status



def logout():
    app.storage.user.clear()
    ui.navigate.to('/')

def on_favorite_toggle(value: bool, is_favorite: bool, recipe_id: str):
    payload = {"user_name": app.storage.user.get("user_id"),"recipe_id": recipe_id}
    
    if value:
        post("http://127.0.0.1:8090/user/favorites/add", json=payload)
    elif not value and is_favorite:
        post("http://127.0.0.1:8090/user/favorites/remove", json=payload)

def on_rate_change(e, recipe_id: str, rating_component, recipe):
    payload = {
        "new_rate": e.value,
        "user_id": app.storage.user.get("user_id"),
        "recipe_id": recipe_id
    }

    response = post("http://127.0.0.1:8090/recipe/rate", json=payload)

    if response.status_code == status.HTTP_400_BAD_REQUEST:
        ui.notify("כבר דירגת מתכון זה", color="red")
        ui.navigate.to(f"/Recipe/{recipe_id}")
        return

    if response.status_code == status.HTTP_200_OK:
        ui.navigate.to(f"/Recipe/{recipe_id}")


        

@ui.page('/Recipe/{recipe_id}', title="Recipe", favicon='Images/logo3.jpg')
def Recipe_page(recipe_id: str):
    ui.add_head_html("<div dir=rtl>")
    ui.query('body').classes('bg-[#f4f1ea]')

    # ====== טעינת מתכון ======
    response = get(f"http://127.0.0.1:8090/recipe/id/{recipe_id}")
    recipe = response.json()

    # ====== בדיקה אם במועדפים ======
    user_id = app.storage.user.get("user_id")
    favorites = get(
        f"http://127.0.0.1:8090/user/favorites/{user_id}"
    ).json()

    is_favorite = str(recipe_id) in favorites['favorites']

    # ====== Drawer ======
    drawer = ui.drawer('left', bordered=True).classes('bg-[#f4f1ea] w-48')
    with drawer:
        ui.label('תפריט ראשי').classes('text-lg font-bold mb-4 text-[#4a3c2a]')
        ui.button('בית', on_click=lambda: ui.navigate.to('/PersonalPage')) \
            .classes('block mb-2 text-[#4a3c2a]')
        ui.button('התנתקות', on_click=logout) \
            .classes('block mb-2 text-[#4a3c2a]')

    # ====== Header ======
    with ui.row().classes('w-full bg-[#f0ece1] p-3 items-center shadow-md'):
        with ui.row().classes('flex-1 justify-start'):
            ui.icon('menu') \
                .classes('text-2xl cursor-pointer text-[#4a3c2a]') \
                .on('click', drawer.toggle)

        with ui.row().classes('flex-1 justify-center'):
            ui.image("Images/logo3.jpg") \
                .classes('w-16 h-16 object-contain')

        with ui.row().classes('flex-1'):
            pass

    # ====== תוכן ======
    with ui.column().classes('items-center w-full mt-8'):
        with ui.card().classes('w-[600px] bg-white shadow-md rounded-xl p-6'):

            # ====== אישור אדמין ======
            if app.storage.user.get("is_admin") and 'pending' in recipe['status']:
                with ui.row().classes('justify-center gap-4 mb-4'):
                    ui.button('אישור', color='green', icon='check')
                    ui.button('דחייה', color='red', icon='close')

            with ui.row().classes('items-center justify-between w-full'):
                already_rated = app.storage.user.get("user_id") in recipe['rated_user']
                with ui.row().classes('gap-1'):
                    rating = ui.rating(
                        value=round(recipe['rate']),
                        size="md",
                        color="yellow",
                        on_change=lambda e: on_rate_change(e, recipe['_id'], rating, recipe),
                    ).classes('material-icons text-yellow-500 cursor-pointer')
                    if already_rated:
                        rating.disable()


                ui.image(
                    f"http://127.0.0.1:8090/recipe/file/{recipe['_id']}"
                ).classes('w-64 h-48 object-cover rounded-lg')

                # ====== כפתור מועדפים ======
                favorite_chip = ui.chip(
                    selectable=True,
                    selected=is_favorite,
                    icon='bookmark',
                    color='orange',
                    on_selection_change=lambda e: on_favorite_toggle(e.value, is_favorite, recipe['_id'])
                ).classes(
                    'material-icons cursor-pointer'
                )


                with ui.column().classes('gap-1'):
                    ui.label(f"קטגוריה: {recipe['recipeType']}") \
                        .classes('text-md font-semibold text-[#4a3c2a]')
                    ui.label(f"רמת קושי: {recipe['difficulty']}") \
                        .classes('text-md font-semibold text-[#4a3c2a]')

            ui.label(recipe['recipeName']) \
                .classes('text-xl font-bold text-[#4a3c2a] text-center mt-4')

            # ====== מצרכים ======
            ui.label('מצרכים:') \
                .classes('text-lg font-semibold text-[#4a3c2a] mt-4 mb-2')

            with ui.column().classes('gap-2'):
                for item in recipe['ingredients']:
                    ui.checkbox(item)

            # ====== הוראות ======
            ui.label('הוראות הכנה:') \
                .classes('text-lg font-semibold text-[#4a3c2a] mt-6 mb-2')

            ui.label(recipe['recipe']) \
                .classes('text-sm text-[#6b5e4a] whitespace-pre-line')

        # ====== תגובות ======
        ui.label('תגובות') \
            .classes('text-xl font-bold text-[#4a3c2a] mt-8 mb-4')

        comments_column = ui.column().classes('w-[600px] gap-4')
        username = recipe['userName']

        def add_comment():
            text = comment_input.value.strip()
            if text:
                timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
                with comments_column:
                    with ui.card().classes(
                        'w-full bg-[#faf7f2] p-3 rounded-lg shadow-sm'
                    ):
                        ui.label(f"{username} · {timestamp}") \
                            .classes('text-sm font-bold text-[#4a3c2a]')
                        ui.label(text) \
                            .classes('text-sm text-[#6b5e4a]')
                comment_input.value = ''

        with ui.row().classes('w-[600px] gap-2 mt-2'):
            comment_input = ui.input(placeholder='הוסף תגובה...') \
                .classes('flex-1')
            ui.button('שלח', on_click=add_comment) \
                .classes('bg-[#4a3c2a] text-white rounded-lg px-4 py-2')



