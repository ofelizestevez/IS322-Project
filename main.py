import os
import json
from dotenv import load_dotenv
from VideoGameSearchParser import VideoGameSearchParser
from RawgAPI import RAWGAPI
from Chatter import Chatter

class ChatProcessor:
    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv("OPEN_AI_KEY")
        self.MODEL = "gpt-3.5-turbo-0125"
        self.RAWG_API_KEY = os.getenv("RAWG_API_KEY")
        self.TEMPERATURE = 0.0

        self.chatter_llm = Chatter(self.API_KEY, self.MODEL, self.TEMPERATURE)
        self.search_llm = VideoGameSearchParser(self.API_KEY, self.MODEL, self.TEMPERATURE)
        self.rawg_api = RAWGAPI(self.RAWG_API_KEY)

    def process_chat(self, chat_history):
        chat_request = chat_history[-1]
        chat_response = self.chatter_llm.parse_request(chat_request, chat_history[:-1])
        chat_response_json = json.loads(chat_response.content)

        response = {"Chatter": chat_response_json}
        chat_history.append(chat_request)

        if chat_response_json["search"]:
            search_response = self.search_llm.parse_request(chat_response_json["search"])
            response["Searcher"] = json.loads(search_response.content)

            genres = response["Searcher"]["genres"]
            tags = response["Searcher"]["tags"]

            api_response = self.rawg_api.query_rawg(genres=genres, tags=tags)
            game_titles = []
            if api_response:
                games = api_response["results"]
                for game in games:
                    game_titles.append(game["name"])
                response["Games"] = game_titles
            else:
                response["Error"] = "Error querying RAWG API."

        return response

# Example usage:
if __name__ == "__main__":
    chat_processor = ChatProcessor()
    chatter_history = []
    while True:
        chat_request = input("you: ").strip()
        chatter_history.append(chat_request)
        response = chat_processor.process_chat(chatter_history)
        print(json.dumps(response, indent=4))
