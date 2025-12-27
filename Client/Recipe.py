from nicegui import ui
from datetime import datetime


@ui.page('/Recipe',title="Recipe",favicon='Images/logo3.jpg')
def Recipe_page():
    ui.add_head_html("<div dir=rtl>")
    ui.query('body').classes('bg-[#f4f1ea]')

    drawer = ui.drawer('left', bordered=True).classes('bg-[#f4f1ea] w-48')
    with drawer:
        ui.label('תפריט ראשי').classes('text-lg font-bold mb-4 text-[#4a3c2a]')
        ui.link('בית', '#').classes('block mb-2 text-[#4a3c2a]')
        ui.link('התנתקות', '#').classes('block mb-2 text-[#4a3c2a]')

    with ui.row().classes('w-full bg-[#f0ece1] p-3 items-center shadow-md'):
        with ui.row().classes('flex-1 justify-start'):
            ui.icon('menu').classes('text-2xl cursor-pointer text-[#4a3c2a]').on('click', drawer.toggle)
        with ui.row().classes('flex-1 justify-center'):
            ui.image("Images/logo3.jpg").classes('w-16 h-16 object-contain')
        with ui.row().classes('flex-1'):  
            pass

    with ui.column().classes('items-center w-full mt-8'):
        with ui.card().classes('w-[600px] bg-white shadow-md rounded-xl p-6'):

            # === כפתורי אישור ודחייה (למנהל) ===
            with ui.row().classes('justify-center gap-4 mb-4'):
                ui.button('אישור', color='green', icon='check').classes('px-4 py-2 text-white rounded-lg shadow-md')
                ui.button('דחייה', color='red', icon='close').classes('px-4 py-2 text-white rounded-lg shadow-md')

            # שורה עם דירוג (ימין), תמונה (מרכז), מועדפים (שמאל) + dropdowns בעמודה נוספת
            with ui.row().classes('items-center justify-between w-full'):
                # דירוג
                with ui.row().classes('gap-1'):
                    ui.rating(value=0, size="md").classes('material-icons text-yellow-500 cursor-pointer')

                # תמונה
                ui.image("https://tekoafarms.co.il/wp-content/uploads/2024/10/5-1-860x643.jpg").classes(
                    'w-64 h-48 object-cover rounded-lg'
                )

                # מועדפים
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

            ui.label('שם המתכון').classes('text-xl font-bold text-[#4a3c2a] text-center mt-4')

            ui.label('מצרכים:').classes('text-lg font-semibold text-[#4a3c2a] mt-4 mb-2')
            ingredients = [
                "2 כוסות קמח",
                "1/2 כוס סוכר",
                "3 ביצים",
                "1/2 כוס שמן",
                "1 כפית אבקת אפייה",
                "1/2 כפית מלח",
            ]
            with ui.column().classes('gap-2'):
                for item in ingredients:
                    ui.checkbox(item)

            ui.label('הוראות הכנה:').classes('text-lg font-semibold text-[#4a3c2a] mt-6 mb-2')
            instructions = """1. מערבבים בקערה את כל המצרכים היבשים.
    2. מוסיפים את הביצים והשמן ולשים עד קבלת בצק אחיד.
    3. מניחים לנוח חצי שעה.
    4. אופים בתנור שחומם מראש ל־180° במשך 25 דקות.
    """
            ui.label(instructions).classes('text-sm text-[#6b5e4a] whitespace-pre-line')
            
            ui.button('העלה', color='#4a3c2a').classes('mt-6 px-6 py-2 text-white rounded-lg shadow-md')

        ui.label('תגובות').classes('text-xl font-bold text-[#4a3c2a] mt-8 mb-4')

        comments_column = ui.column().classes('w-[600px] gap-4')
        
        # שם משתמש קבוע בקוד
        username = "נויה"

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


