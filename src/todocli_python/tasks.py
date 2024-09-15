import click
from storage import Task, init_db
from sqlalchemy import insert


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    ctx.obj["engine"] = init_db()


@cli.command()
@click.argument("description")
@click.pass_context
def add(ctx, description: str) -> None:
    """tasks add <description>"""
    with ctx.obj["engine"].connect() as conn:
        stmt = insert(Task).values(description=description)
        conn.execute(stmt)
        conn.commit()


if __name__ == "__main__":

    cli(obj={})
