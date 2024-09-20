from datetime import datetime
import click
import sqlalchemy
from storage import Task, init_db
from sqlalchemy import Engine, insert, select, update

from time_since_created import elapsed_time_str

from prettytable.colortable import ColorTable, Themes


def show_tasks(tasks: list[tuple[int, str, datetime]]):
    table = ColorTable(["ID", "Description", "Created"], theme=Themes.MINE)

    for task in tasks:
        table.add_row((task[0], task[1], elapsed_time_str(task[2])))

    table.align = "l"
    print(table)


@click.group()
@click.pass_context
def cli(ctx) -> None:
    ctx.ensure_object(dict)
    engine: Engine = init_db()
    ctx.obj["engine"] = engine


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


@cli.command()
@click.argument("description")
@click.pass_context
def add(ctx, description: str) -> None:
    """Add a new task to your list"""
    with ctx.obj["engine"].connect() as conn:
        stmt = insert(Task).values(description=description)
        conn.execute(stmt)
        conn.commit()


@cli.command
@click.option(
    "-a", "--all", is_flag=True, default=False, help="Also list completed tasks."
)
@click.pass_context
def list(ctx, all: bool) -> None:
    """List uncompleted tasks"""
    tasks = get_tasks(ctx.obj["engine"], all)
    show_tasks(tasks)


@cli.command
@click.pass_context
@click.argument("id")
def complete(ctx, id: str) -> None:
    with ctx.obj["engine"].connect() as conn:
        stmt = update(Task).where(Task.id == id).values({"completed": True})
        conn.execute(stmt)
        conn.commit()


@cli.command
@click.pass_context
@click.argument("id")
def delete(ctx, id: str) -> None:
    with ctx.obj["engine"].connect() as conn:
        stmt = sqlalchemy.delete(Task).where(Task.id == id)
        conn.execute(stmt)
        conn.commit()


if __name__ == "__main__":
    cli(obj={})
