from nicegui import ui
import re

ui.add_head_html("<div dir=rtl>")
ui.query('body').classes('bg-[#ede7d5]')

with ui.column().classes('items-center justify-center h-full w-full '):
    with ui.card().classes(
        'w-[450px] p-6 rounded-2xl shadow-md bg-[#f0ece1] border border-[#e8e2d8] overflow-hidden'
    ):
        with ui.row().classes('items-center justify-center mb-6'):
            ui.image("logo3.jpg").classes(
                'w-20 h-20 object-contain ml-3'
            )
            ui.label('התחברות').classes(
                'text-3xl font-bold text-[#4a3c2a]'
            )

        # Tabs: Login / Signup
        with ui.row().classes('justify-center mb-4'):
            ui.button('הרשמה').classes(
                'bg-[#e0c9a6] text-[#4a3c2a] font-semibold px-6 py-2 rounded-full'
            ).disable()
            ui.button('התחברות').classes(
                'bg-[#e8e2d8] text-[#a39b90] font-semibold px-6 py-2 rounded-full cursor-not-allowed'
            )

        # First & Last name in one row
        with ui.row().classes('w-full mb-3'):
            ui.input(placeholder="שם משתמש").classes('flex-1 rounded-xl bg-white text-[#4a3c2a]')

        # Password
        with ui.row().classes('w-full mb-3'):
            password = ui.input(
                placeholder="סיסמה",
                password=True,
                password_toggle_button=True,
                validation={"": lambda v: True}, #so it will match to the other password input in the site
            ).classes('flex-1 rounded-xl bg-white text-[#4a3c2a]')
           

        # Login Button
        ui.button('התחבר', on_click=lambda: ui.notify('!התחברת בהצלחה')).classes(
            'mt-4 bg-[#e0c9a6] hover:bg-[#cbb08c] text-[#4a3c2a] font-semibold rounded-xl px-4 py-2 w-full shadow-sm'
        )

        # Forgot password link
        with ui.row().classes('justify-center mt-2 w-full'):
            ui.link('שכחתי סיסמה', '#').classes(
                'text-sm text-[#6b5b4c] hover:text-[#d97706] hover:underline transition-colors duration-300'
            )
ui.run()
