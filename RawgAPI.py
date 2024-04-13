import requests

class RAWGAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.rawg.io/api/games"

    def _build_query(self, genres=[], tags=[]):
        query_string = ""
        if genres:
            query_string += f"&genres={','.join(genres)}"
        if tags:
            query_string += f"&tags={','.join(tags)}"
        return query_string

    def query_rawg(self, genres=[], tags=[]):
        query_string = self._build_query(genres=genres, tags=tags)
        url = f"{self.base_url}?key={self.api_key}{query_string}"
        try:
            response = requests.get(url)
            return response.json()
        except Exception as e:
            print("Error:", e)
            return None