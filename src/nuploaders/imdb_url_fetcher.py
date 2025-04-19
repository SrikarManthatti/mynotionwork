import requests
from typing import Optional #for type hinting


class IMDBFetcher():
    def __init__(self, base_link: str):
        self.base_link = base_link
        self.headers = {'User-Agent': 'Mozilla/5.0'} #using it to mimic browser, else IMDB return 403 client error
        self.ref = "?ref_=fn_all_ttl_1"
    
    def generate_link(self, titleid: str) -> str:
        return _validate_imdb_url(f"{self.base_link}/title/{titleid}/{self.ref}")
    
    def _validate_imdb_url(self, link: str) -> str:
        response = requests.get(link, headers = self.headers)
        response.raise_for_status()
        return link


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
        







