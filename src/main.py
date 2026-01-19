import sys
import time
from src.api import get_live_matches
from src.formatter import print_matches
from src.config import load_config

VERSION = "1.1.0"


def parse_args():
    """Parse command line arguments and return configuration
        
        This function parses the command line arguments provided by the user
        and returns a dictionary with the parsed configuration options.
        """
    # Load config to get default refresh interval
    config = load_config()
    default_refresh_interval = config.get("refresh_interval", 30)
    
    args = {
        "command": None,
        "refresh": False,
        "refresh_interval": default_refresh_interval,  # seconds
        "filter_term": config.get("default_filter", None),
        "show_help": False,
        "show_version": False
    }
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg in ("--help", "-h"):
            args["show_help"] = True
        elif arg == "version":
            args["show_version"] = True
        elif arg == "live":
            args["command"] = "live"
        elif arg == "--refresh" and i + 1 < len(sys.argv):
            args["refresh"] = True
            try:
                args["refresh_interval"] = int(sys.argv[i + 1])
                i += 1  # Skip next argument since we consumed it
            except ValueError:
                print(f"Invalid refresh interval: {sys.argv[i + 1]}")
                sys.exit(1)
        elif arg == "--refresh":
            args["refresh"] = True
        elif arg == "--filter" and i + 1 < len(sys.argv):
            args["filter_term"] = sys.argv[i + 1].lower()
            i += 1  # Skip next argument since we consumed it
        else:
            args["command"] = arg  # Unknown command
        
        i += 1
    
    return args


def filter_matches(matches, filter_term):
    """Filter matches based on the filter term"""
    if not filter_term:
        return matches
    
    filtered = []
    for match in matches:
        # Check if filter term is in match name (case insensitive)
        if filter_term in match["name"].lower():
            filtered.append(match)
    
    return filtered


def refresh_matches(refresh_interval, filter_term=None):
    """Continuously refresh and display matches"""
    try:
        while True:
            # Clear screen (works on most terminals)
            print("\033[2J\033[H", end="")  # ANSI escape codes to clear screen and move cursor to top-left
            
            print(f"🔄 Auto-refreshing every {refresh_interval} seconds. Press Ctrl+C to stop.\n")
            
            matches = get_live_matches()
            
            # Apply filter if specified
            if filter_term:
                matches = filter_matches(matches, filter_term)
                if not matches:
                    print(f"No matches found containing '{filter_term}'")
                    time.sleep(refresh_interval)
                    continue
            
            print_matches(matches)
            time.sleep(refresh_interval)
    except KeyboardInterrupt:
        print("\n🛑 Auto-refresh stopped by user.")
        sys.exit(0)


def main():
    args = parse_args()
    
    if args["show_help"] or len(sys.argv) < 2:
        print("""
Cricket CLI — Real-time live cricket scores

Usage:
  cricket live                           Show live matches
  cricket live --refresh                Auto-refresh live matches every 30 seconds
  cricket live --refresh <seconds>       Auto-refresh live matches every <seconds> seconds
  cricket live --filter <team>           Filter matches containing <team> name
  cricket version                        Show version information
  cricket --help                         Show this help
  cricket -h                             Show this help
""")
        sys.exit(0)

    if args["show_version"]:
        print(f"Cricket CLI Version {VERSION}")
        sys.exit(0)

    if args["command"] == "live":
        # Handle auto-refresh if requested
        if args["refresh"]:
            refresh_matches(args["refresh_interval"], args["filter_term"])
        else:
            matches = get_live_matches()
            
            # Apply filter if specified
            if args["filter_term"]:
                matches = filter_matches(matches, args["filter_term"])
                if not matches:
                    print(f"No matches found containing '{args['filter_term']}'")
                    sys.exit(0)
            
            print_matches(matches)
            sys.exit(0)

    print("Unknown command")
    sys.exit(1)


if __name__ == "__main__":
    main()
