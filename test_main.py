import pytest
from datetime import datetime, timedelta
from main import TodoApp, TodoItem

# Fixture to set up the TodoApp instance
@pytest.fixture
def todo_app():
    return TodoApp()

def test_add_todo(todo_app):
    """Test adding a new to-do item"""
    description = "Test To-Do"
    due_date = datetime.now() + timedelta(days=1)
    todo_app.todos.append(TodoItem(description, due_date))

    assert len(todo_app.todos) == 1
    assert todo_app.todos[0].description == description
    assert todo_app.todos[0].due_date == due_date
    assert not todo_app.todos[0].done

def test_show_pending_todos(todo_app, capsys):
    """Test showing pending to-dos"""
    todo_app.todos.append(TodoItem("Pending To-Do", datetime.now() + timedelta(days=1)))
    todo_app.show_pending_todos()

    captured = capsys.readouterr()
    assert "Pending To-Do" in captured.out
    assert "Pending" in captured.out

def test_mark_done(todo_app, capsys):
    """Test marking a to-do as done"""
    todo_app.todos.append(TodoItem("To-Do to be marked done", datetime.now() + timedelta(days=1)))

    # Mock user input to mark the first to-do as done
    todo_app.todos[0].mark_done()

    assert todo_app.todos[0].done is True

def test_show_past_todos(todo_app, capsys):
    """Test showing past to-dos"""
    todo_app.todos.append(TodoItem("Past To-Do", datetime.now() - timedelta(days=1)))
    todo_app.show_past_todos()

    captured = capsys.readouterr()
    assert "Past To-Do" in captured.out
    assert "Overdue" in captured.out

def test_todo_overdue_status(todo_app):
    """Test the overdue status of a to-do item"""
    overdue_todo = TodoItem("Overdue To-Do", datetime.now() - timedelta(days=1))
    todo_app.todos.append(overdue_todo)

    assert overdue_todo.is_overdue() is True

def test_todo_marked_done_status(todo_app):
    """Test marking a to-do as done and checking its status"""
    done_todo = TodoItem("Done To-Do", datetime.now() + timedelta(days=1))
    todo_app.todos.append(done_todo)
    done_todo.mark_done()

    assert done_todo.done is True
    assert done_todo.is_overdue() is False

def test_view_today_todos(todo_app, capsys):
    """Test viewing today's to-dos"""
    todo_app.todos.append(TodoItem("Today's To-Do", datetime.now()))
    todo_app.show_view(1, "Today's To-Dos")

    captured = capsys.readouterr()
    assert "Today's To-Do" in captured.out

def test_view_week_todos(todo_app, capsys):
    """Test viewing this week's to-dos"""
    todo_app.todos.append(TodoItem("This Week's To-Do", datetime.now() + timedelta(days=2)))
    todo_app.show_view(7, "This Week's To-Dos")

    captured = capsys.readouterr()
    assert "This Week's To-Do" in captured.out

def test_view_month_todos(todo_app, capsys):
    """Test viewing this month's to-dos"""
    todo_app.todos.append(TodoItem("This Month's To-Do", datetime.now() + timedelta(days=10)))
    todo_app.show_view(30, "This Month's To-Dos")

    captured = capsys.readouterr()
    assert "This Month's To-Do" in captured.out
