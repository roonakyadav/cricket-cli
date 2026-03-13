🏏 Cricket CLI — Live Cricket Scores in Terminal

A Python-based Command Line Interface (CLI) tool that displays live cricket match information directly in the terminal.
The project uses real-time web scraping with multi-source fallback and a clean terminal UI.

🚀 Features

📡 Fetches live cricket match data (real-time when available)

🌐 Usess web scraping (no paid APIs required)

🔁 Multi-source fallback (Cricbuzz → ESPN)

🛡️ Graceful degradation if sources are blocked or no matches are live

🖥️ Clean, readable terminal table output using rich

🧪 Safe execution (never crashes due to network issues)

🧠 How It Works (High Level)

CLI command cricket live is executed

Tool tries to scrape Cricbuzz live scores

If blocked/unavailable → falls back to ESPN public JSON

If both fail → shows a user-friendly message

Results are rendered as a formatted table in terminal

This approach demonstrates real-world defensive engineering.

📂 Project Structure
cricket-cli/
│
├── cricket                 # CLI entrypoint
├── requirements.txt
├── README.md
│
└── src/
    ├── __init__.py
    ├── main.py             # CLI command handling
    ├── api.py              # Scraping & data fetching logic
    └── formatter.py        # Terminal UI rendering

⚙️ Installation & Setup
1️⃣ Clone / Open Project
cd cricket-cli

2️⃣ Create Virtual Environment
python3 -m venv .venv

3️⃣ Activate Virtual Environment
source .venv/bin/activate


You should see:

(.venv)

4️⃣ Install Dependencies
pip install -r requirements.txt

5️⃣ Make the cricket script executable
chmod +x cricket

6️⃣ Install additional packages if needed
pip install pip-tools

7️⃣ Verify installation
python -c "import requests, bs4, lxml, rich; print('Dependencies installed successfully')"

▶️ Usage
Show live matches
python ./cricket live


or

./cricket live

Additional commands:
./cricket --help          # Show help information
./cricket -h              # Short help
./cricket version         # Show version information
./cricket live --refresh  # Auto-refresh live matches
./cricket live --filter india  # Filter matches containing 'india'

Examples:
./cricket live                    # View all live matches
./cricket live --refresh 30       # Refresh every 30 seconds
./cricket live --filter australia # Filter for Australia matches

🖥️ Sample Output
🏏 Live Cricket Matches

+----------------------------------+------+-------+-------------------------------+
| Match                            | Type | Venue | Status                        |
+----------------------------------+------+-------+-------------------------------+
| India vs Australia               | Live | N/A   | India need 42 runs in 5 overs |
+----------------------------------+------+-------+-------------------------------+


If no live matches or sites are blocked:

Live matches temporarily unavailable
Source sites blocked or no live games

🛠️ Technologies Used

Python 3

requests — HTTP requests

beautifulsoup4 + lxml — Web scraping

rich — Terminal UI rendering

Virtual Environments (venv)

⚠️ Troubleshooting & Notes

Common Issues:
• If getting HTTP errors, sites may be temporarily blocking requests
• Try running the command again after a few minutes
• Ensure all dependencies are installed (check with pip list)

Notes on Web Scraping:
• Scraping is done only on public, unauthenticated pages
• Requests are low-frequency (CLI usage)
• Some sites may temporarily block automated requests
• The tool handles this safely without crashing

Rate Limiting:
• Tool makes minimal requests (only when called)
• No persistent connections or aggressive scraping
• Respects site robots.txt guidelines

🎓 Academic / Interview Explanation (Short)

“This project is a Python CLI tool that fetches live cricket data by scraping public sources. It uses a fallback mechanism to handle blocking or downtime and displays results in a clean terminal interface.”

📌 Possible Enhancements

Auto-refresh (watch mode)

Match filtering by team

Local caching

API-based integration if available

Packaging for PyPI

👤 Author

Ronak Yadav
Scaler School of Technology, Bangalore
Computer Science Student

LinkedIn: [ronak-yadav](https://linkedin.com/in/ronak-yadav)
GitHub: [roonakyadav_](https://github.com/roonakyadav_)
Email: roonakyadav@gmail.com
