import datetime
from pathlib import Path

import typer
from git import Repo  # type: ignore

app = typer.Typer()

DIARY_PATH = Path("README.md")

REPO_PATH = Path.cwd()


class LifeEntry:
    def __init__(self, date: datetime.date, summary: str, description: str = None):
        self.date = date
        self.summary = summary
        description = "" if description is None else description
        self.description = description

    def __str__(self):
        return f"# {self.date.strftime('%Y-%m-%d')}\n{self.summary}\n{self.description}\n\n"


@app.command()
def review() -> None:
    repo = Repo(REPO_PATH)
    commits = repo.iter_commits("--all")
    for commit in commits:
        authored_date = typer.style(
            commit.authored_datetime.astimezone().strftime("%Y-%m-%d"),
            fg=typer.colors.BRIGHT_CYAN,
        )
        summary = typer.style(commit.summary, fg=typer.colors.BRIGHT_BLUE)
        msg = f"{authored_date} : {summary}"
        typer.echo(msg)


@app.command()
def today() -> None:
    date_str = typer.style(
        datetime.date.today().strftime("%d %B %Y"),
        fg=typer.colors.BRIGHT_CYAN,
        bold=True,
    )
    typer.echo(f"On day {date_str}")


@app.command()
def commit(
    date: datetime.datetime = typer.Option(None, help="Date for the life update", prompt=True),
    summary: str = typer.Option("", help="Commit Summary", prompt=True),
    description: str = typer.Option(None, help="Description", prompt=True),
) -> None:

    repo = Repo(REPO_PATH)
    if date is None:
        date = datetime.date.today()

    prev_text = ""
    if DIARY_PATH.exists():
        prev_text = DIARY_PATH.read_text()

    new_entry = LifeEntry(date=date, summary=summary, description=description)
    new_text = str(new_entry) + prev_text

    DIARY_PATH.write_text(new_text)

    # Add new version of `DIARY_PATH`
    repo.git.add(DIARY_PATH)

    if description is None:
        repo.git.commit("-m", summary, "--date", date)
    else:
        repo.git.commit("-m", summary, "-m", description, "--date", date)


def run() -> None:
    app()


if __name__ == "__main__":
    run()
