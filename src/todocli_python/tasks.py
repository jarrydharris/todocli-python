from datetime import datetime
import click
import sqlalchemy
from storage import Task, init_db
from sqlalchemy import Engine, insert, select, text, update

from time_since_created import elapsed_time_str

from prettytable.colortable import ColorTable, Themes

# ================================================================
# This section contains the core functionality.
# ================================================================


def get_db_time(engine: Engine) -> datetime:
    with engine.connect() as conn:
        stmt = "SELECT DATETIME('now', 'localtime');"
        time = conn.execute(text(stmt)).fetchone()
    return time[0]


def add_task(engine: Engine, description: str):
    with engine.connect() as conn:
        stmt = insert(Task).values(description=description)
        conn.execute(stmt)
        conn.commit()


def show_tasks(tasks: list[tuple[int, str, datetime]]):
    table = ColorTable(["ID", "Description", "Created"], theme=Themes.MINE)

    for task in tasks:
        table.add_row((task[0], task[1], elapsed_time_str(task[2])))

    table.align = "l"
    print(table)


def get_tasks(engine: Engine, all: bool) -> list[tuple[int, str, datetime]]:
    stmt = select(Task.id, Task.description, Task.created)
    if not all:
        stmt = stmt.where(Task.completed == False)
    with engine.connect() as conn:
        tasks: tuple[int, str, datetime] = conn.execute(stmt).fetchall()
    return tasks


def get_task(engine: Engine, id: int) -> tuple[int, str, datetime]:
    stmt = select(Task.id, Task.description, Task.created).where(Task.id == id)
    with engine.connect() as conn:
        tasks: tuple[int, str, datetime] = conn.execute(stmt).fetchall()
    return tasks


def complete_task(engine: Engine, id: int):
    with engine.connect() as conn:
        stmt = update(Task).where(Task.id == id).values({"completed": True})
        conn.execute(stmt)
        conn.commit()


def delete_task(engine: Engine, id: int):
    with engine.connect() as conn:
        stmt = sqlalchemy.delete(Task).where(Task.id == id)
        conn.execute(stmt)
        conn.commit()


# ================================================================
# This section contains the CLI functionality.
# ================================================================


@click.group()
@click.pass_context
def cli(ctx) -> None:
    ctx.ensure_object(dict)
    engine: Engine = init_db()
    ctx.obj["engine"] = engine


@cli.command()
@click.argument("description")
@click.pass_context
def add(ctx, description: str) -> None:
    """Add a new task to your to-do list"""
    add_task(ctx.obj["engine"], description)


@cli.command
@click.option(
    "-a",
    "--all",
    is_flag=True,
    default=False,
    help="Display pending AND completed tasks.",
)
@click.pass_context
def list(ctx, all: bool) -> None:
    """Display all pending tasks that haven't been completed"""
    print(get_db_time(ctx.obj["engine"]))
    tasks = get_tasks(ctx.obj["engine"], all)
    show_tasks(tasks)


@cli.command
@click.pass_context
@click.argument("id")
def complete(ctx, id: str) -> None:
    "Mark a specific task as completed"
    complete_task(ctx.obj["engine"], id)
    show_tasks(get_task(ctx.obj["engine"], id))


@cli.command
@click.pass_context
@click.argument("id")
def delete(ctx, id: str) -> None:
    "Permanently remove a task from your list"
    delete_task(ctx.obj["engine"], id)
    show_tasks(get_task(ctx.obj["engine"], id))


if __name__ == "__main__":
    cli(obj={})
