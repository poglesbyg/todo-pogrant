from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt

console = Console()

# To-Do List Item Class
class TodoItem:
    def __init__(self, description, due_date):
        self.description = description
        self.due_date = due_date
        self.done = False

    def mark_done(self):
        self.done = True

    def is_overdue(self):
        return datetime.now() > self.due_date and not self.done

# To-Do List Application Class
class TodoApp:
    def __init__(self):
        self.todos = []

    def add_todo(self):
        description = Prompt.ask("Enter the task description")
        due_date_str = Prompt.ask(
            "Enter the due date (YYYY-MM-DD HH:MM) or press Enter for today",
            default=datetime.now().strftime("%Y-%m-%d %H:%M")
        )
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d %H:%M")
            self.todos.append(TodoItem(description, due_date))
            console.print("[green]To-do item added successfully![/green]")
        except ValueError:
            console.print("[red]Invalid date format. Please use YYYY-MM-DD HH:MM[/red]")

    def show_todos(self, filter_func=None, title="All To-Dos", show_index=False):
        table = Table(title=title)
        if show_index:
            table.add_column("No.", style="cyan", justify="right")
        table.add_column("Description", style="cyan")
        table.add_column("Due Date", style="magenta")
        table.add_column("Status", style="yellow")

        filtered_todos = list(filter(filter_func, self.todos))
        for index, todo in enumerate(filtered_todos, start=1):
            status = "Done" if todo.done else "Overdue" if todo.is_overdue() else "Pending"
            row = [str(index), todo.description, todo.due_date.strftime("%Y-%m-%d %H:%M"), status] if show_index else [todo.description, todo.due_date.strftime("%Y-%m-%d %H:%M"), status]
            table.add_row(*row)

        console.print(table)
        return filtered_todos

    def show_pending_todos(self):
        self.show_todos(lambda todo: not todo.done and todo.due_date > datetime.now(), "Pending To-Dos")

    def show_past_todos(self):
        self.show_todos(lambda todo: todo.due_date < datetime.now(), "Past To-Dos")

    def show_view(self, days, title):
        now = datetime.now()
        end_date = now + timedelta(days=days)
        self.show_todos(lambda todo: not todo.done and now <= todo.due_date <= end_date, title)

    def mark_done(self):
        pending_todos = self.show_todos(lambda todo: not todo.done, "Mark a To-Do as Done", show_index=True)

        if not pending_todos:
            console.print("[yellow]No pending to-dos available to mark as done.[/yellow]")
            return

        index = IntPrompt.ask("Enter the number of the to-do to mark as done (or 0 to cancel)")
        
        if 0 < index <= len(pending_todos):
            todo_to_mark = pending_todos[index - 1]
            todo_to_mark.mark_done()
            console.print(f"[green]To-do '{todo_to_mark.description}' marked as done![/green]")
        elif index == 0:
            console.print("[yellow]Operation cancelled.[/yellow]")
        else:
            console.print("[red]Invalid selection.[/red]")

    def run(self):
        while True:
            console.print("\n[bold]To-Do List Menu[/bold]")
            console.print("1. Add a new to-do item")
            console.print("2. View pending to-dos")
            console.print("3. View past to-dos")
            console.print("4. View today’s to-dos")
            console.print("5. View this week’s to-dos")
            console.print("6. View this month’s to-dos")
            console.print("7. Mark a to-do as done")
            console.print("8. Exit")

            choice = IntPrompt.ask("Choose an option")

            if choice == 1:
                self.add_todo()
            elif choice == 2:
                self.show_pending_todos()
            elif choice == 3:
                self.show_past_todos()
            elif choice == 4:
                self.show_view(1, "Today's To-Dos")
            elif choice == 5:
                self.show_view(7, "This Week's To-Dos")
            elif choice == 6:
                self.show_view(30, "This Month's To-Dos")
            elif choice == 7:
                self.mark_done()
            elif choice == 8:
                console.print("[bold green]Goodbye![/bold green]")
                break
            else:
                console.print("[red]Invalid choice. Please try again.[/red]")

# Main script execution
if __name__ == "__main__":
    app = TodoApp()
    app.run()
    