import os
import json
from dotenv import load_dotenv
from VideoGameSearchParser import VideoGameSearchParser
from RawgAPI import RAWGAPI
from Chatter import Chatter

load_dotenv()

API_KEY = os.getenv("OPEN_AI_KEY")
MODEL  = "gpt-3.5-turbo-0125"
RAWG_API_KEY = os.getenv("RAWG_API_KEY")
TEMPERATURE = 0.0

# Create an instance of the VideoGameSearchParser class
chatter_llm = Chatter(API_KEY, MODEL, TEMPERATURE)
search_llm = VideoGameSearchParser(API_KEY, MODEL, TEMPERATURE)
rawg_api = RAWGAPI(RAWG_API_KEY)
chatter_history = []

while True:
    chat_request = input("you: ").strip()
    
    chat_response = chatter_llm.parse_request(chat_request, chatter_history)
    chat_response_json = json.loads(chat_response.content)
    
    print("")
    print("Chatter: ")
    print(chat_response_json)
    print("")
    
    chatter_history.append(chat_request)
    
    if(chat_response_json["search"]):
        print("")
        print("Sending to Searcher:")
        print(chat_response_json["search"])
        print("")
        print("Searcher:")
        search_response = search_llm.parse_request(chat_response_json["search"])
        print(search_response.content)
        search_response_json = json.loads(search_response.content)
        print("")
        
        genres = search_response_json["genres"]
        tags = search_response_json["tags"]
        
        api_response = rawg_api.query_rawg(genres=genres, tags=tags)
        game_titles = []
        if api_response:
            print()
            print("Games recommended: ")
            games = api_response["results"]
            for game in games:
                game_titles.append(game["name"])
                print(game["name"])
            print()
        else:
            print("Error querying RAWG API.")
            
        chatter_history.append("The search has given this list of games: " + " ".join(game_titles))