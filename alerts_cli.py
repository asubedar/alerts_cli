import os
import click
import requests
from tabulate import tabulate

API_URL = os.getenv('ALERTS_API_URL', 'http://localhost:5005')

@click.group()
def cli():
    """A CLI to access the Alerts API."""
    pass

# GET /consolidated_holdings
@click.command()
def get_holdings():
    """Fetch and display all consolidated holdings."""
    response = requests.get(f"{API_URL}/consolidated_holdings")
    if response.status_code == 200:
        holdings = response.json()
        if holdings:
            table = [
                [
                    holding.get("symbol"),
                    holding.get("avg_price"),
                    holding.get("close"),
                    holding.get("current_value"),
                    holding.get("net"),
                    holding.get("net_chg"),
                    holding.get("total_cost_basis"),
                    holding.get("total_shares"),
                ]
                for holding in holdings
            ]
            headers = [
                "Symbol", "Avg Price", "Close", "Current Value",
                "Net", "Net Change", "Total Cost Basis", "Total Shares"
            ]
            click.echo(tabulate(table, headers, tablefmt="pretty"))
        else:
            click.echo("No holdings found.")
    else:
        click.echo("Failed to fetch holdings.")

# GET /alerts
@click.command()
def get_alerts():
    """Fetch and display all alerts."""
    response = requests.get(f"{API_URL}/alerts")
    if response.status_code == 200:
        alerts = response.json()
        if alerts:
            table = [
                [
                    alert.get("symbol"),
                    alert.get("alert_type"),
                    alert.get("alert_direction"),
                    alert.get("alert_level"),
                    alert.get("note"),
                    alert.get("fire_date"),
                ]
                for alert in alerts
            ]
            headers = ["Symbol", "Type", "Direction", "Level", "Note", "Fired"]
            click.echo(tabulate(table, headers, tablefmt="pretty"))
        else:
            click.echo("No alerts found.")
    else:
        click.echo("Failed to fetch alerts.")

# POST /alerts
@click.command()
@click.option('--symbol', prompt='Symbol', help='The symbol for the alert')
@click.option('--alert_type', prompt='Alert Type', help='The type of alert')
@click.option('--alert_direction', prompt='Alert Direction', help='The direction of the alert')
@click.option('--alert_level', prompt='Alert Level', help='The alert level(s), comma-separated')
def create_alert(symbol, alert_type, alert_direction, alert_level):
    """Create a new alert."""
    data = {
        "symbol": symbol,
        "alert_type": alert_type,
        "alert_direction": alert_direction,
        "alert_level": alert_level
    }
    response = requests.post(f"{API_URL}/alerts", json=data)
    if response.status_code == 201:
        click.echo("Alert created successfully.")
    else:
        click.echo(f"Failed to create alert: {response.json().get('error')}")

# PUT /alerts/<id>
@click.command()
@click.argument('id')
@click.option('--symbol', prompt='Symbol', help='The symbol for the alert')
@click.option('--alert_type', prompt='Alert Type', help='The type of alert')
@click.option('--alert_direction', prompt='Alert Direction', help='The direction of the alert')
@click.option('--alert_level', prompt='Alert Level', help='The alert level')
@click.option('--note', prompt='Note', help='A note for the alert')
def update_alert(id, symbol, alert_type, alert_direction, alert_level, note):
    """Update an existing alert."""
    data = {
        "symbol": symbol,
        "alert_type": alert_type,
        "alert_direction": alert_direction,
        "alert_level": alert_level,
        "note": note
    }
    response = requests.put(f"{API_URL}/alerts/{id}", json=data)
    if response.status_code == 200:
        click.echo("Alert updated successfully.")
    else:
        click.echo(f"Failed to update alert: {response.json().get('error')}")

# DELETE /alerts/<id>
@click.command()
@click.argument('id')
def delete_alert(id):
    """Delete an alert by ID."""
    response = requests.delete(f"{API_URL}/alerts/{id}")
    if response.status_code == 200:
        click.echo("Alert deleted successfully.")
    else:
        click.echo(f"Failed to delete alert: {response.json().get('error')}")

# Add commands to the CLI group
cli.add_command(get_holdings)
cli.add_command(get_alerts)
cli.add_command(create_alert)
cli.add_command(update_alert)
cli.add_command(delete_alert)

if __name__ == "__main__":
    cli()
