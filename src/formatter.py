from rich.console import Console
from rich.table import Table
from rich.style import Style
from rich.text import Text

console = Console()


def get_status_color(status):
    """Determine color based on match status"""
    status_lower = status.lower()
    if 'live' in status_lower or 'batting' in status_lower:
        return "green"
    elif 'complete' in status_lower or 'won' in status_lower or 'result' in status_lower:
        return "blue"
    elif 'scheduled' in status_lower or 'toss' in status_lower:
        return "yellow"
    elif 'delayed' in status_lower or 'rain' in status_lower:
        return "red"
    else:
        return "white"


def print_matches(matches):
    table = Table(title="🏏 Live Cricket Matches")

    table.add_column("Match", style="bold")
    table.add_column("Type")
    table.add_column("Venue")
    table.add_column("Status")

    for m in matches:
        # Colorize status based on match condition
        status_text = Text(m["status"])
        status_color = get_status_color(m["status"])
        status_text.stylize(status_color, 0, len(m["status"]))
        
        table.add_row(
            m["name"],
            m["type"],
            m["venue"],
            status_text
        )

    console.print(table)
