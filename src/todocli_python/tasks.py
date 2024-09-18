import click
import sqlalchemy
from storage import Task, init_db
from sqlalchemy import Engine, insert, select, update


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
    """Add a new task to your list"""
    with ctx.obj["engine"].connect() as conn:
        stmt = insert(Task).values(description=description)
        conn.execute(stmt)
        conn.commit()


@cli.command
@click.pass_context
def list(ctx) -> None:
    """List uncompleted tasks"""
    with ctx.obj["engine"].connect() as conn:
        stmt = select(Task).where(Task.completed == False)
        tasks = conn.execute(stmt).fetchall()
    for task in tasks:
        print(*task)


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
