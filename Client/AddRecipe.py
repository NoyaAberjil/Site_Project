from nicegui import ui, app
from datetime import datetime
from PersonalPage import load_all_recipes, load_user_recipes, load_admin_recipes

def logout():
    app.storage.user.clear()
    ui.navigate.to('/')

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
                with ui.row().classes('gap-1'):
                    ui.rating(value=0, size="md").classes('material-icons text-yellow-500 cursor-pointer')

                ui.image("https://tekoafarms.co.il/wp-content/uploads/2024/10/5-1-860x643.jpg").classes(
                    'w-64 h-48 object-cover rounded-lg'
                )

            
                ui.chip(selectable=True, icon='bookmark', color='orange').classes(
                    'material-icons text-orange-500 cursor-pointer'
                )

                # עמודה עם שני dropdowns
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
            ui.textarea(
                label='מצרכים',
                placeholder='כתוב כאן את רשימת המצרכים, פסיק אחרי כל מצרך...'
            ).classes('w-full').props('rows=6 mt-2')

            # === תיבת טקסט להוראות הכנה ===
            ui.textarea(
                label='הוראות הכנה',
                placeholder='כתוב כאן את שלבי ההכנה...'
            ).classes('w-full mt-4').props('rows=8')
        comments_column = ui.column().classes('w-[600px] gap-4')

        # שם משתמש קבוע בקוד
        username = app.storage.user.get("user_id")
            
        ui.button('העלה', color='#4a3c2a').classes('mt-6 px-6 py-2 text-white rounded-lg shadow-md')

