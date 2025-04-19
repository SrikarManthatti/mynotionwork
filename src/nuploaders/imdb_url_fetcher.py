import requests
from typing import Optional #for type hinting


class IMDBFetcher():
    pass

@dataclass
class Movie():
    """This is a data class which I am using to create a data structure for movie"""
    title: str
    runtime: str
    genre: str
    ratings: list
    imdbrating: float
    imdbid: str


class OMDBClient():
    """This class will be used to fetch the movie details from omdb"""
    
    def __init__(self, api_key: str, base_link: str):
        self.api_key = api_key
        self.base_link = base_link
    
    def fetch_movie(self, movie_name) -> Optional[Movie]:
        params = {"t": movie_name, "apikey": self.api_key}

        try:
            response = requests.get(self.base_link, params = params, timeout = 10)
            response.raise_for_status()
        except requests.RequestException as re:
            log.Error("Error in fetching information for movie: %s", self.movie_name)
            return None
        
        data = response.json()
        # check EXAMPLES at https://www.omdbapi.com/ to get sample response
        if data.get("Response") == "True":
            return Movie(
                title = data.get("Title", "N/A")
                runtime = data.get("Runtime", "N/A")
                genre =  data.get("Genre", "N/A")
                ratings =  data.get("Ratings", []) 
                imdbrating =  data.get("imdbRating","N/A")
                imdbid =  data.get("imdbID","N/A")
            )
        







