from rich.console import Console
from rich.table import Table

console = Console()


def print_matches(matches):
    table = Table(title="🏏 Live Cricket Matches")

    table.add_column("Match", style="bold")
    table.add_column("Type")
    table.add_column("Venue")
    table.add_column("Status")

    for m in matches:
        table.add_row(
            m["name"],
            m["type"],
            m["venue"],
            m["status"]
        )

    console.print(table)
