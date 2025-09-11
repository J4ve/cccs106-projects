import flet as ft
import mysql.connector
from db_connection import connect_db



def main(page: ft.Page):
    page.title = "User Login"
    page.theme_mode=ft.ThemeMode.LIGHT  # force to light mode to fix dark mode bad ui
    page.window.frameless = True
    page.window.height = 350
    page.window.width = 400
    page.bgcolor = ft.Colors.AMBER_ACCENT
    page.window.center()
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def button_clicked(e):
        page.update()


    page.add(
        ft.Text(
                    "User Login",
                    size=20, 
                    weight=ft.FontWeight.BOLD
                ),
        ft.TextField(
                        label="Username", 
                        hint_text="Enter your username",
                        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
                    ),
        ft.TextField(
                        label="Password", 
                        hint_text="Enter your password",
                        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
                    ),
        ft.ElevatedButton(text="Submit", on_click=button_clicked),
    )

    # counter = ft.Text("0", size=50, data=0)

    # def increment_click(e):
    #     counter.data += 1
    #     counter.value = str(counter.data)
    #     counter.update()

    # page.floating_action_button = ft.FloatingActionButton(
    #     icon=ft.Icons.ADD, on_click=increment_click
    # )
    # page.add(
    #     ft.SafeArea(
    #         ft.Container(
    #             counter,
    #             alignment=ft.alignment.center,
    #         ),
    #         expand=True,
    #     )
    # )


ft.app(main)
