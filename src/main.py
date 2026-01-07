import sys
from src.api import get_live_matches
from src.formatter import print_matches


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h"):
        print("""
Cricket CLI — Real-time live cricket scores

Usage:
  cricket live        Show live matches
  cricket --help      Show help
""")
        sys.exit(0)

    if sys.argv[1] == "live":
        matches = get_live_matches()
        print_matches(matches)
        sys.exit(0)

    print("Unknown command")
    sys.exit(1)


if __name__ == "__main__":
    main()
