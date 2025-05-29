# ClashBot

## Overview
ClashBot is a Discord bot designed to enhance the League of Legends Clash tournament experience by providing opponent research capabilities. The bot helps teams gather and analyze information about their opponents, giving them a strategic advantage in their Clash matches.

## Features
- Opponent research for League of Legends Clash tournaments
- Discord integration for easy team communication
- Automated data retrieval from Riot Games API
- User-friendly command interface with `##` prefix

## Prerequisites
- Python 3.8 or higher
- Discord account and bot token
- Riot Games API key
- Discord server with appropriate permissions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ClashBot.git
cd ClashBot
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your credentials:
```
BOT_KEY=your_discord_bot_token
RIOT_API_KEY=your_riot_api_key
```

## Usage

1. Start the bot:
```bash
python main.py
```

2. Once the bot is running, you can use it in your Discord server with the `##` command prefix.

## Project Structure
```
ClashBot/
├── main.py           # Bot entry point and setup
├── src/             # Source code directory
│   ├── ClashBot.py  # Main bot implementation
│   └── league/      # League of Legends API integration
├── tests/           # Test files
├── logs/            # Log files
└── requirements.txt # Project dependencies
```

## Development
- The bot is built using discord.py library
- Uses Python's asyncio for asynchronous operations
- Implements rate limiting for Riot Games API compliance
- Stores API response templates in `src/league/file` directory

## Contributing
1. Fork the repository
2. Create a new branch for your feature
3. Submit a pull request with a description of your changes

## License
[Add your license information here]

## Acknowledgments
- Riot Games API
- Discord.py library
- All contributors and testers
