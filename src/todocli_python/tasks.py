import click
from storage import Task, init_db
from sqlalchemy import Engine, insert, select


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
    """tasks add \"Task description\" """
    with ctx.obj["engine"].connect() as conn:
        stmt = insert(Task).values(description=description)
        conn.execute(stmt)


@cli.command
@click.pass_context
def list(ctx) -> None:
    """tasks list"""
    with ctx.obj["engine"].connect() as conn:
        stmt = select(Task.__table__)
        tasks = conn.execute(stmt).fetchall()
    for task in tasks:
        print(*task)


if __name__ == "__main__":

    cli(obj={})
