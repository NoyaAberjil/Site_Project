from nicegui import ui
import re

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
            ui.input(placeholder="אימייל של המשתמש").classes('flex-1 rounded-xl bg-white text-[#4a3c2a]')


ui.run()
