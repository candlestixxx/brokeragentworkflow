import click
from notifications import notify_all
import models

@click.group()
def cli():
    """One-Minute Manager: Daily Goals CLI."""
    pass

def get_db_path():
    """Fallback backwards compat function since we removed it from models.py"""
    import os
    return os.getenv("DATABASE_PATH", "goals.db")

@cli.command()
def init():
    """Initialize the goals database."""
    url = models.get_db_url()
    models.init_db()
    click.echo(f"Initialized database at {url}")

@cli.command()
@click.argument('description')
def add(description):
    """Add a new one-minute goal."""
    models.add_goal(description)
    click.echo(f"Added goal: '{description}'")
    notify_all(
        subject="New Goal Added",
        body=f"You added a new goal: {description}",
        speakable_message=f"You added a new goal: {description}"
    )

@cli.command()
def list():
    """List all pending one-minute goals."""
    goals = models.list_pending_goals()
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
    success = models.complete_goal(goal_id)
    if not success:
        click.echo(f"No goal found with ID {goal_id}.")
    else:
        click.echo(f"Goal {goal_id} marked as completed! Excellent work.")
        notify_all(
            subject="Goal Completed!",
            body=f"Excellent work! You completed goal {goal_id}.",
            speakable_message=f"Excellent work! You completed goal {goal_id}."
        )

@cli.command()
@click.argument('quarter')
@click.argument('description')
def add_initiative(quarter, description):
    """Add a new quarterly initiative (e.g. Q4 "Holiday mailers")."""
    models.add_initiative(quarter, description)
    click.echo(f"Added quarterly initiative for {quarter}: '{description}'")
    notify_all(
        subject="New Initiative Added",
        body=f"You added a new initiative for {quarter}: {description}",
        speakable_message=f"You added a new quarterly initiative for {quarter}: {description}"
    )

@cli.command()
def list_initiatives():
    """List all pending quarterly initiatives."""
    initiatives = models.list_pending_initiatives()
    if not initiatives:
        click.echo("No pending initiatives.")
        return

    click.echo("Pending Quarterly Initiatives:")
    for init in initiatives:
        click.echo(f"[{init[0]}] {init[1]}: {init[2]}")

@cli.command()
@click.argument('initiative_id', type=int)
def complete_initiative(initiative_id):
    """Mark a quarterly initiative as complete."""
    success = models.complete_initiative(initiative_id)
    if not success:
        click.echo(f"No initiative found with ID {initiative_id}.")
    else:
        click.echo(f"Initiative {initiative_id} marked as completed!")
        notify_all(
            subject="Initiative Completed!",
            body=f"Great job completing quarterly initiative {initiative_id}.",
            speakable_message=f"Great job completing quarterly initiative {initiative_id}."
        )

if __name__ == '__main__':
    models.init_db()
    cli()
