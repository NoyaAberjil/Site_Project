from nicegui import ui



@ui.page('/PersonalPage',title="PersonalPage",favicon='Images/logo3.jpg')
def PersonalPage_page():
    ui.add_head_html("<div dir=rtl>")
    ui.query('body').classes('bg-[#f4f1ea]')

    drawer = ui.drawer('left', bordered=True).classes('bg-[#f4f1ea] w-48')
    with drawer:
        ui.label('תפריט ראשי').classes('text-lg font-bold mb-4 text-[#4a3c2a]')
        ui.link('בית', '#').classes('block mb-2 text-[#4a3c2a]')
        ui.link('פרופיל', '#').classes('block mb-2 text-[#4a3c2a]')
        ui.link('מועדפים', '#').classes('block mb-2 text-[#4a3c2a]')
        ui.link('הוספת מתכון', '/Recipe').classes('block mb-2 text-[#4a3c2a]')
        ui.link('התנתקות', '#').classes('block mb-2 text-[#4a3c2a]')

    with ui.row().classes('w-full bg-[#f0ece1] p-3 items-center shadow-md'):
        with ui.row().classes('flex-1 justify-start'):
            ui.icon('menu').classes('text-2xl cursor-pointer text-[#4a3c2a]').on('click', drawer.toggle)

        with ui.row().classes('flex-1 justify-center'):
            ui.image("Images/logo3.jpg").classes('w-16 h-16 object-contain')

        with ui.row().classes('flex-1'):  
            pass

    # ------------------ TWO DROPDOWNS ------------------
    with ui.row().classes('justify-center gap-4 w-full mt-4 mb-6'):
        category_dropdown = ui.select(
            ['כל המתכונים', 'מתוק', 'מלוח', 'דיאטטי','כשר'],
            value='כל המתכונים',
            label='קטגוריה'
        ).classes('w-48')

        difficulty_dropdown = ui.select(
            ['קל', 'בינוני', 'קשה'],
            value='קל',
            label='רמת קושי'
        ).classes('w-48')

        # CARDS
        for i in range(0, 10, 3):  
            with ui.row().classes('justify-center gap-4 w-full'):
                for j in range(3):
                    if i + j < 10:  
                        with ui.card().classes('w-96 bg-[#ffffff] shadow-md p-4 rounded-xl cursor-pointer'):
                            ui.label('נויה').classes('text-lg font-bold text-[#4a3c2a] text-center')
                            ui.label('שם המתכון').classes('text-sm text-[#6b5e4a] text-center mb-3')
                            ui.image(
                                "https://tekoafarms.co.il/wp-content/uploads/2024/10/5-1-860x643.jpg"
                            ).classes('w-full object-contain rounded-lg mb-3').on("click", lambda:ui.navigate.to("/Recipe"))

                            with ui.row().classes('justify-between items-center w-full'):
                                with ui.row().classes('gap-1'):
                                    ui.rating(value=0, size="md")
                                ui.chip(selectable=True, icon='bookmark', color='orange')

                            with ui.row().classes('justify-center items-center w-full'):
                                ui.button('תגובות').classes('bg-[#e0c9a6] text-[#4a3c2a] rounded-lg px-4 py-1')


