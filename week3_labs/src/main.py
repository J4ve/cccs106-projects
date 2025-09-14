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

    username = ft.TextField(
                    label="Username", 
                    hint_text="Enter your username",
                    bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
                )
    password = ft.TextField(
                    label="Password",
                    password=True,
                    hint_text="Enter your password",
                    bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
                )
    
    # ---- DIALOGS

    success_dialog = ft.AlertDialog(title=f"Login Successful",
                                    alignment=ft.alignment.center,
                                    content=f"Welcome {username}",
                                    actions=[
                                        ft.TextButton("OK", on_click=lambda e: page.close(invalid_input_dialog))
                                    ]
                                    )
    failure_dialog = ft.AlertDialog(title="Login Failed",
                                    
                                    )
    invalid_input_dialog = ft.AlertDialog(title="Input Error",
                                            content=ft.Text("Please enter username and password"),
                                            alignment=ft.alignment.center,
                                            actions=[
                                                ft.TextButton("OK", on_click=lambda e: page.close(invalid_input_dialog))
                                            ]
                                            )
    database_error_dialog = ft.AlertDialog(title="Database Error",
                                            
                                            )
    
    async def login_click(e):
        print("clicked") # test ko lang if gumagana yung pag click ng submit

        try:
            connect_db()
            if username.value and password.value != "":
                page.open(success_dialog)
            else:
                page.open(invalid_input_dialog)
        except mysql.connector.Error as e:
            page.open(failure_dialog)

        page.update()


    page.add(
        ft.Text(
            "User Login",
            size=20, 
            weight=ft.FontWeight.BOLD
        ),
        username,
        password,
        ft.ElevatedButton(text="Submit", on_click=login_click),
    )

ft.app(main)
