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
    
    # ---- DIALOGS ----
    current_dialog = None

    def close_dialog(e):
        nonlocal current_dialog     # i'm currently trying out the nonlocal keyword
        if current_dialog:          # also, i'm trying to use this function as an experiment (closing dialogs)
            page.close(current_dialog)   # (alternative for lambda functions inside each dialog actions)
            page.update()
            current_dialog = None

    success_dialog = ft.AlertDialog(title=f"Login Successful",
                                    alignment=ft.alignment.center,
                                    content=f"Welcome {username}",
                                    actions=[
                                        ft.TextButton("OK", on_click=close_dialog)
                                    ]
                                    )
                                    
    failure_dialog = ft.AlertDialog(title="Login Failed",
                                    
                                    )
    invalid_input_dialog = ft.AlertDialog(title="Input Error",
                                            content=ft.Text("Please enter username and password"),
                                            alignment=ft.alignment.center,
                                            actions=[
                                                ft.TextButton("OK", on_click=close_dialog)
                                            ]
                                            )
    database_error_dialog = ft.AlertDialog(title="Database Error",
                                            
                                        )

    async def login_click(e):
        nonlocal current_dialog
        print("Submit clicked log") # test ko lang if gumagana yung pag click ng submit

        try:
            connect_db()
            if username.value and password.value != "":
                current_dialog = success_dialog
            else:
                current_dialog = invalid_input_dialog


        except mysql.connector.Error as e:
            current_dialog = failure_dialog
        
        page.open(current_dialog)
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
