import click
import sqlite3
import os
from dotenv import load_dotenv
from notifications import notify_all

load_dotenv()

def get_db_path():
    return os.getenv("DATABASE_PATH", "goals.db")

def init_db(db_path=None):
    if db_path is None:
        db_path = get_db_path()
    """Initialize the database with the goals table."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@click.group()
def cli():
    """One-Minute Manager: Daily Goals CLI."""
    pass

@cli.command()
def init():
    """Initialize the goals database."""
    db_path = get_db_path()
    init_db(db_path)
    click.echo(f"Initialized database at {db_path}")

@cli.command()
@click.argument('description')
def add(description):
    """Add a new one-minute goal."""
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    c.execute('INSERT INTO goals (description) VALUES (?)', (description,))
    goal_id = c.lastrowid
    conn.commit()
    conn.close()
    click.echo(f"Added goal: '{description}'")
    notify_all(
        subject="New Goal Added",
        body=f"You added a new goal: {description}",
        speakable_message=f"You added a new goal: {description}"
    )

@cli.command()
def list():
    """List all pending one-minute goals."""
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    c.execute('SELECT id, description FROM goals WHERE status = "pending"')
    goals = c.fetchall()
    conn.close()

    if not goals:
        click.echo("No pending goals. Great job!")
        return

    click.echo("Pending One-Minute Goals:")
    for goal in goals:
        click.echo(f"[{goal[0]}] {goal[1]}")

@cli.command()
@click.argument('goal_id', type=int)
def complete(goal_id):
    """Mark a one-minute goal as complete."""
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    c.execute('UPDATE goals SET status = "completed" WHERE id = ?', (goal_id,))
    if c.rowcount == 0:
        click.echo(f"No goal found with ID {goal_id}.")
    else:
        click.echo(f"Goal {goal_id} marked as completed! Excellent work.")
        notify_all(
            subject="Goal Completed!",
            body=f"Excellent work! You completed goal {goal_id}.",
            speakable_message=f"Excellent work! You completed goal {goal_id}."
        )
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    cli()
