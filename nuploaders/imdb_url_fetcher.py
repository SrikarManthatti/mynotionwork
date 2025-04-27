import httpx
import os
from typing import Optional #for type hinting
from dataclasses import dataclass
from nuploaders import CONFIG, log



class IMDBFetcher(): #make a cache folder to load url quickly instead of hitting api everytime
    def __init__(self, base_link: str):
        self.base_link = base_link
        self.headers = {'User-Agent': 'Mozilla/5.0'} #using it to mimic browser, else IMDB return 403 client error
        self.ref = "?ref_=fn_all_ttl_1"
    
    async def generate_link(self, titleid: str) -> str:
            log.info("Validating URL for titleid: %s", titleid)
            return await self._validate_imdb_url(f"{self.base_link}/title/{titleid}/{self.ref}")
    
    async def _validate_imdb_url(self, link: str) -> str:
            async with httpx.AsyncClient() as client:
                response = await client.get(link, headers = self.headers)
                response.raise_for_status()
            return link


@dataclass
class Movie():
    """This is a data class which I am using to create a data structure for movie"""
    title: str
    runtime: str
    mycategory: str
    genre: str
    ratings: list
    imdbrating: float
    imdbid: str
    imdblink: str


class OMDBClient():
    """This class will be used to fetch the movie details from omdb"""
    
    def __init__(self, base_link: str):
        self.api_key = os.getenv("OMDB_API_KEY") #api_key
        self.base_link = base_link
    
    async def fetch_movie(self, movie_name, mycategory) -> Optional[Movie]:
            params = {"t": movie_name, "apikey": self.api_key}

            try:
                async with httpx.AsyncClient() as asycclient:
                    response = await asycclient.get(self.base_link, params = params, timeout = 10)
                    log.info("Response received for movie %s ", movie_name)
                response.raise_for_status()
            except httpx.RequestError as re:
                log.Error("Error in fetching information for movie: %s", movie_name)
                return None

            imdb_obj = IMDBFetcher(CONFIG["imdb"]["base_link"]) #pass config value
            data = response.json()
            # check EXAMPLES at https://www.omdbapi.com/ to get sample response
            if data.get("Response") == "True":
                return Movie(
                    title = data.get("Title", "N/A"),
                    runtime = data.get("Runtime", "N/A"),
                    mycategory = mycategory,
                    genre =  data.get("Genre", "N/A"),
                    ratings =  data.get("Ratings", []), 
                    imdbrating =  data.get("imdbRating","N/A"),
                    imdbid =  data.get("imdbID","N/A"),
                    imdblink = await imdb_obj.generate_link(data.get("imdbID","N/A")),
                )
        







