# GPT Video Game Searcher

## Overview
The primary objective of this project is to create a chatbot that interfaces with features from a Steam-like website seamlessly, all while conversing with the user. This proof-of-concept showcases a chatbot designed to recommend new video games to the user. This has been achieved by utilizing 2 GPT models and the RAWG API (a comprehensive video game database with a RESTful API).

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
- Basics of using a chatbot to do API queries.
- Basics of creating a structured data chatbot with ways to export data in a JSON-like manner.

## Future Plans
- Implement a full web interface for users to chat with online.
- Enhance the Searcher API to be a comprehensive RAWG API chatbot, utilizing more API calls such as [https://api.rawg.io/api/games/{id}](https://api.rawg.io/api/games/{id}) to show details of a game and have better interactions with the API.

## Thank You
Thank you for your interest in this project!
