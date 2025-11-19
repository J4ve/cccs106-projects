"""
Simple Task Manager App - Flet Demo
A cross-platform task management application demonstrating Flet's capabilities
"""

import flet as ft
from datetime import datetime


class Task:
    def __init__(self, name, priority="Medium"):
        self.name = name
        self.priority = priority
        self.completed = False
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")


class TaskManagerApp:
    def __init__(self):
        self.tasks = []
    
    def main(self, page: ft.Page):
        # Page configuration
        page.title = "Task Manager Pro - Group 7"
        page.window.width = 400
        page.window.height = 700
        page.window.resizable = True
        page.padding = 20
        page.theme_mode = ft.ThemeMode.LIGHT
        page.scroll = "auto"
        
        # Header
        def toggle_theme(e):
            page.theme_mode = (
                ft.ThemeMode.DARK 
                if page.theme_mode == ft.ThemeMode.LIGHT 
                else ft.ThemeMode.LIGHT
            )
            theme_icon.icon = (
                ft.Icons.DARK_MODE 
                if page.theme_mode == ft.ThemeMode.LIGHT 
                else ft.Icons.LIGHT_MODE
            )
            page.update()
        
        theme_icon = ft.IconButton(
            icon=ft.Icons.DARK_MODE,
            on_click=toggle_theme,
            tooltip="Toggle theme"
        )
        
        header = ft.Row(
            controls=[
                ft.Icon(ft.Icons.TASK_ALT, size=32, color=ft.Colors.BLUE),
                ft.Text(
                    "Task Manager Pro",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE
                ),
                theme_icon
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        
        # Statistics
        stats_text = ft.Text(
            "Total: 0 | Completed: 0 | Pending: 0",
            size=14,
            color=ft.Colors.GREY_700
        )
        
        def update_stats():
            total = len(self.tasks)
            completed = sum(1 for task in self.tasks if task.completed)
            pending = total - completed
            stats_text.value = f"Total: {total} | Completed: {completed} | Pending: {pending}"
        
        # Task input section
        task_input = ft.TextField(
            hint_text="Enter your task...",
            expand=True,
            border_color=ft.Colors.BLUE_200,
            focused_border_color=ft.Colors.BLUE,
        )
        
        priority_dropdown = ft.Dropdown(
            label="Priority",
            options=[
                ft.dropdown.Option("High"),
                ft.dropdown.Option("Medium"),
                ft.dropdown.Option("Low"),
            ],
            value="Medium",
            width=120,
            border_color=ft.Colors.BLUE_200,
        )
        
        # Task list
        task_list = ft.Column(spacing=10, scroll="auto")
        
        def create_task_card(task, index):
            def toggle_task(e):
                task.completed = not task.completed
                update_task_display()
            
            def delete_task(e):
                self.tasks.pop(index)
                update_task_display()
            
            priority_colors = {
                "High": ft.Colors.RED_200,
                "Medium": ft.Colors.ORANGE_200,
                "Low": ft.Colors.GREEN_200,
            }
            
            return ft.Card(
                content=ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Checkbox(
                                value=task.completed,
                                on_change=toggle_task,
                                active_color=ft.Colors.BLUE
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        task.name,
                                        size=16,
                                        weight=ft.FontWeight.W_500,
                                        color=ft.Colors.GREY_500 if task.completed else None,
                                        style=ft.TextStyle(
                                            decoration=ft.TextDecoration.LINE_THROUGH 
                                            if task.completed else None
                                        )
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.Container(
                                                content=ft.Text(
                                                    task.priority,
                                                    size=12,
                                                    color=ft.Colors.BLACK87
                                                ),
                                                bgcolor=priority_colors[task.priority],
                                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                                border_radius=10,
                                            ),
                                            ft.Text(
                                                task.created_at,
                                                size=11,
                                                color=ft.Colors.GREY_600
                                            )
                                        ],
                                        spacing=10
                                    )
                                ],
                                spacing=5,
                                expand=True
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                icon_color=ft.Colors.RED_400,
                                on_click=delete_task,
                                tooltip="Delete task"
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    padding=10,
                ),
                elevation=2,
            )
        
        def update_task_display():
            task_list.controls.clear()
            if not self.tasks:
                task_list.controls.append(
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Icon(ft.Icons.INBOX, size=64, color=ft.Colors.GREY_400),
                                ft.Text(
                                    "No tasks yet!",
                                    size=18,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Text(
                                    "Add your first task above",
                                    size=14,
                                    color=ft.Colors.GREY_500,
                                    text_align=ft.TextAlign.CENTER
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10
                        ),
                        padding=40,
                        alignment=ft.alignment.center
                    )
                )
            else:
                for idx, task in enumerate(self.tasks):
                    task_list.controls.append(create_task_card(task, idx))
            
            update_stats()
            page.update()
        
        def add_task(e):
            if task_input.value.strip():
                new_task = Task(
                    name=task_input.value.strip(),
                    priority=priority_dropdown.value
                )
                self.tasks.append(new_task)
                task_input.value = ""
                priority_dropdown.value = "Medium"
                update_task_display()
            else:
                snack_bar = ft.SnackBar(
                    content=ft.Text("Please enter a task name!"),
                    bgcolor=ft.Colors.RED_400,
                    open=True
                )
                page.overlay.append(snack_bar)
                page.update()
        
        def clear_completed(e):
            if any(task.completed for task in self.tasks):
                self.tasks = [task for task in self.tasks if not task.completed]
                update_task_display()
                snack_bar = ft.SnackBar(
                    content=ft.Text("Completed tasks cleared!"),
                    bgcolor=ft.Colors.GREEN_400,
                    open=True
                )
                page.overlay.append(snack_bar)
                page.update()
            else:
                snack_bar = ft.SnackBar(
                    content=ft.Text("No completed tasks to clear!"),
                    bgcolor=ft.Colors.ORANGE_400,
                    open=True
                )
                page.overlay.append(snack_bar)
                page.update()
        
        add_button = ft.ElevatedButton(
            text="Add Task",
            icon=ft.Icons.ADD,
            on_click=add_task,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
        )
        
        clear_button = ft.OutlinedButton(
            text="Clear Completed",
            icon=ft.Icons.CLEAR_ALL,
            on_click=clear_completed,
        )
        
        # Layout
        page.add(
            ft.Container(height=10),
            header,
            ft.Divider(height=20, color=ft.Colors.BLUE_200),
            stats_text,
            ft.Container(height=10),
            ft.Text("Add New Task", size=16, weight=ft.FontWeight.W_500),
            ft.Row(
                controls=[task_input, priority_dropdown],
                spacing=10
            ),
            ft.Row(
                controls=[add_button, clear_button],
                spacing=10
            ),
            ft.Container(height=20),
            ft.Text("Your Tasks", size=16, weight=ft.FontWeight.W_500),
            ft.Container(
                content=task_list,
                expand=True,
            ),
        )
        
        # Initialize display
        update_task_display()


# Run the app
def main(page: ft.Page):
    app = TaskManagerApp()
    app.main(page)


if __name__ == "__main__":
    ft.app(target=main)
