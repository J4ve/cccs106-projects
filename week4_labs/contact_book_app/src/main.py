# main.py
import flet as ft
from database import init_db, create_samples_db, delete_all_contacts
from app_logic import display_contacts, add_contact

def main(page: ft.Page):
    page.title = "Contact Book"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 400
    page.window_height = 600
    db_conn = init_db()
    #create_samples_db(db_conn)
    #delete_all_contacts(db_conn)   # I added the functions delete and add sample contacts for test purposes

    def check_theme() -> bool:      # typehint to bool idk gusto ko lang for readability
        if page.theme_mode == ft.ThemeMode.SYSTEM:  # in default its set to ThemeMode.SYSTEM, so i forced DARK mode
            page.theme_mode = ft.ThemeMode.DARK
        if page.theme_mode == ft.ThemeMode.DARK:
            return True
        else:
            return False

    def theme_changed(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        theme_switch.icon = (
            ft.Icons.LIGHT_MODE if check_theme() == False else ft.Icons.DARK_MODE
        )
        theme_switch.text = (
            "Light Mode" if check_theme() == False else "Dark Mode"
        )
        page.update()


        
    theme_switch = ft.ElevatedButton(text="Dark Mode",
                            icon=ft.Icons.DARK_MODE,
                            on_click=theme_changed,
                            )
    
    

    name_input = ft.TextField(label="Name", width=350, error_text=None, icon=ft.Icons.PERSON)
    phone_input = ft.TextField(label="Phone", width=350, icon=ft.Icons.CONTACT_PHONE)
    email_input = ft.TextField(label="Email", width=350, icon=ft.Icons.EMAIL)
    search_input = ft.TextField(label="Search", # I added the search_contact function from app_logic.py for the on_change event
                                width=350, 
                                icon=ft.Icons.SEARCH,
                                on_change=lambda e: display_contacts(page, 
                                                                     contacts_list_view, 
                                                                     db_conn, 
                                                                     search_term=search_input.value
                                                                     )
                                )
    
    inputs = (name_input, phone_input, email_input)
    contacts_list_view = ft.ListView(expand=1, spacing=10, auto_scroll=True)

    add_button = ft.ElevatedButton(
        text="Add Contact",
        on_click=lambda e: add_contact(page, inputs, contacts_list_view, db_conn)
        )
    
    check_theme()

    page.add(
        ft.Container(
            content=ft.Row(
                    [theme_switch],
                    alignment=ft.MainAxisAlignment.END
                ),
            margin=ft.margin.only(top=30) # for mobile devices, sometimes its too high so I added margin on top
        ),

        ft.Column([ft.Text("Enter Contact Details:", size=20, weight=ft.FontWeight.BOLD),
                    name_input,
                    phone_input,
                    email_input,
                    add_button,
                    
                    ft.Divider(),

                    ft.Text("Contacts:", size=20, weight=ft.FontWeight.BOLD),
                    search_input,
                    contacts_list_view,
                    ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
        )
    display_contacts(page, contacts_list_view, db_conn)

if __name__ == "__main__":
    ft.app(target=main)
