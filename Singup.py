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
            ui.label('הרשמה').classes(
                'text-3xl font-bold text-[#4a3c2a]'
            )

        # Tabs: Login / Signup
        with ui.row().classes('justify-center mb-4'):
            ui.button('הרשמה').classes(
                'bg-[#e0c9a6] text-[#4a3c2a] font-semibold px-6 py-2 rounded-full'
            )
            ui.button('התחברות').classes(
                'bg-[#e8e2d8] text-[#a39b90] font-semibold px-6 py-2 rounded-full cursor-not-allowed'
            ).disable()

        # First & Last name in one row
        with ui.row().classes('w-full mb-3'):
            ui.input(placeholder="שם משתמש").classes('flex-1 rounded-xl bg-white text-[#4a3c2a]')
            # ui.input(placeholder="שם משפחה").classes('flex-1 rounded-xl bg-white text-[#4a3c2a]')

        # Email
        ui.input(
            placeholder="כתובת אימייל",
            validation={"אנא הזן כתובת מייל תקינה": lambda value: bool(re.match(r'^[^@]+@[^@]+\.[^@]+$', value))}
        ).classes('w-full mb-3 rounded-xl bg-white text-[#4a3c2a]')

        # Password & Confirm Password
        with ui.row().classes('w-full mb-3'):
            password1 = ui.input(
                placeholder="סיסמה",
                password=True,
                password_toggle_button=True,
                validation={"": lambda v: True}, #so it will match to the other password input in the site
            ).classes('flex-1 rounded-xl bg-white text-[#4a3c2a]')

            password2 = ui.input(
                placeholder="אימות סיסמה",
                password=True,
                password_toggle_button=True,
                validation={"הסיסמאות חייבות להיות תואמות": lambda value: value == password1.value},
            ).classes('flex-1 rounded-xl bg-white text-[#4a3c2a]')            

        # Sign Up Button
        ui.button('הרשם', on_click=lambda: ui.notify('!נרשמת בהצלחה')).classes(
            'mt-4 bg-[#e0c9a6] hover:bg-[#cbb08c] text-[#4a3c2a] font-semibold rounded-xl px-4 py-2 w-full shadow-sm'
        )

ui.run()
