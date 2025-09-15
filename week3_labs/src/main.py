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
                    label="User name", 
                    hint_text="Enter your username",
                    bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
                    icon=ft.Icons.PERSON,
                    autofocus=True,
                    helper_text="This is your unique identifier",
                    width=300 
                )
    password = ft.TextField(
                    label="Password",
                    password=True,
                    hint_text="Enter your password",
                    bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
                    can_reveal_password=True,
                    icon=ft.Icons.PASSWORD,
                    helper_text="This is your secret key",
                    width=300
                )
    

    # ---- DIALOGS (I defined the dialogs outside the login_click(e) so that it 
    # wouldn't be inefficient making the dialogs each click on login)
    success_dialog = ft.AlertDialog(title=f"Login Successful",
                                    content=ft.Text(f"Welcome {username.value}", text_align=ft.TextAlign.CENTER),
                                    alignment=ft.alignment.center,
                                    actions=[
                                        ft.TextButton("OK", on_click=lambda e: page.close(success_dialog))
                                    ],
                                    icon=ft.Icon(name=ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN)
                                    )
    failure_dialog = ft.AlertDialog(title="Login Failed",
                                    content=ft.Text(f"Invalid username and password", text_align=ft.TextAlign.CENTER),
                                    alignment=ft.alignment.center,
                                    actions=[
                                        ft.TextButton("OK", on_click=lambda e: page.close(failure_dialog))
                                    ],
                                    icon=ft.Icon(name=ft.Icons.ERROR, color=ft.Colors.RED)
                                    )
    invalid_input_dialog = ft.AlertDialog(title="Input Error",
                                            content=ft.Text("Please enter username and password", text_align=ft.TextAlign.CENTER),
                                            alignment=ft.alignment.center,
                                            actions=[
                                                ft.TextButton("OK", on_click=lambda e: page.close(invalid_input_dialog))
                                            ],
                                            icon=ft.Icon(name=ft.Icons.INFO, color=ft.Colors.BLUE)
                                            
                                            )
    database_error_dialog = ft.AlertDialog(title="Database Error",
                                            content=ft.Text("An error occurred while connecting to the database"),
                                            actions=[
                                                ft.TextButton("OK", on_click=lambda e: page.close(database_error_dialog))
                                            ]
                                            )

    
    async def login_click(e):
        print(f"Login button clicked") # test if gumagana yung pag click ng login
        try:
            connect = connect_db()
            cursor = connect.cursor()
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username.value, password.value))
            user = cursor.fetchone()
            # print(user)
            # print(username.value) # for test purposes

            if (username.value != "") and (password.value != ""):
                if user != None:
                    success_dialog.content.value = f"Welcome {username.value}"
                    page.open(success_dialog)
                else:
                    page.open(failure_dialog)
            else:
                page.open(invalid_input_dialog)
        except mysql.connector.Error as e:
            page.open(database_error_dialog)

        page.update()


    page.add(
        
        #title
        ft.Text(
            "User Login",
            size=20, 
            weight=ft.FontWeight.BOLD,
            font_family="Arial"
            
        ),

        #container for username, password
        ft.Container(content=ft.Column(controls=[username, password],
                                       spacing=20,
                                       )

                     ),

        #container for the login button
        ft.Container(content=ft.ElevatedButton(text="Login", 
                                               on_click=login_click, 
                                               width=100, 
                                               icon=ft.Icons.LOGIN
                                               ), 
                    alignment=ft.alignment.top_right,
                    margin=ft.margin.only(0,20,40,0)
                    )
        
    )

ft.app(target=main)
