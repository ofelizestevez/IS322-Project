# GPT Video Game Recommender

## Overview
The primary objective of this project is to create a discord chatbot that interfaces with an online video game search engine API to recommend the player some video games. This has been achieved by utilizing 2 GPT models and the RAWG API (a comprehensive video game database with a RESTful API). The user has the ability to chat with the bot by running `main.py`. This has been packaged into a discord chatbot for a better user experience.

## Bot Usage

### Prerequisites

Before running the bot, ensure you have Python 3.x installed on your system.

### Setup

1. Clone this repository to your local machine.
2. Navigate to the project directory in your terminal.
3. Install the required Python dependencies by running.
4. Create an .env file inside of the project directory with the following
    - OPEN_AI_KEY: API key from openAI
    - RAWG_API_KEY: API key from RAWG
    - DISCORD_TOKEN: token for a discord chat bot.

### Running the Bot

1. Execute the following command in your terminal:
    - ```python bot.py```
2. Your bot should now be online and ready to respond to messages in Discord.

### Interacting with the Bot

Once the bot is running, you can send the first message for the bot to reply to! 

**BONUS**: the bot remembers your previous messages!

## Chatter
- **GPT-3.5 Model**
- **Expects:**
  - Schema
  - User Request
  - Chat History
- **Structured Data:**
  - Response: Your usual chatbot response
  - SearchQuery: A simple GPT prompt created using a summary of the user’s conversation with the player.

## Searcher
- **GPT-3.5 Model**
- **Expects:**
  - Schema
  - User Request
- **Structured Data:**
  - IncludedGenres: Array of API genres
  - IncludedTags: Array of API tags

## RAWG API
- Uses the [RAWG API](https://api.rawg.io/api/games) to search for video games.
- Query parameters for genres and tags are utilized.

## Lessons Learned
- How to use the OpenAI gpt api.
- How to create a gpt chatbot that uses structured data.
- How to create a discord chat-bot.

## Problems
- There were times when the bot wouldn't use the structured data that it was assigned.
  - Interestingly enough, this problem would reoccur more often when using GPT4, so I settled on using GPT 3.5

