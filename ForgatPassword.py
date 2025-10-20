from nicegui import ui
import re


@ui.page('/ForgatPassword',title="ForgatPassword",favicon='Images/logo3.jpg')
def ForgatPassword_page():
    ui.add_head_html("<div dir=rtl>")
    ui.query('body').classes('bg-[#ede7d5]')

    with ui.column().classes('items-center justify-center h-full w-full '):
        with ui.card().classes(
            'w-[450px] p-6 rounded-2xl shadow-md bg-[#f0ece1] border border-[#e8e2d8] overflow-hidden'
        ):
            with ui.row().classes('items-center justify-center mb-6'):
                ui.image("Images/logo3.jpg").classes(
                    'w-20 h-20 object-contain ml-3'
                )
                ui.label('שכחתי סיסמה').classes(
                    'text-3xl font-bold text-[#4a3c2a]'
                )

            # Tabs: Login / Signup
            with ui.row().classes('justify-center mb-4'):
                ui.button('הרשמה',on_click=lambda: ui.navigate.to("/Singup")).classes(
                    'bg-[#e0c9a6] text-[#4a3c2a] font-semibold px-6 py-2 rounded-full'
                ).disable()
                ui.button('התחברות',on_click=lambda: ui.navigate.to("/")).classes(
                    'bg-[#e8e2d8] text-[#a39b90] font-semibold px-6 py-2 rounded-full cursor-not-allowed'
                )

            # First & Last name in one row
            with ui.row().classes('w-full mb-3'):
                ui.input(placeholder="אימייל של המשתמש").classes('flex-1 rounded-xl bg-white text-[#4a3c2a]')
                 # Sign Up Button
            ui.button('שלח', on_click=lambda:ui.navigate.to("/")).classes(
                'mt-4 bg-[#e0c9a6] hover:bg-[#cbb08c] text-[#4a3c2a] font-semibold rounded-xl px-4 py-2 w-full shadow-sm'
            )


