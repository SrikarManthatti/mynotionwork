import requests
from bs4 import BeautifulSoup
from typing import Optional #for type hinting
from urllib.parse import quote

class IMDBFetcher():
    def __init__(self, movie_name: str):
        self.base_link = "https://www.imdb.com"
        self.movie_name = _quote_movie_name(movie_name)
    
    def _quote_movie_name(self, movie):
        return quote(movie)
    
    def fetch_imdb_url(self) -> Optional[str]:
        """This function will use BeautifulSoup to fetch the IMDB URL of a movie"""
        search_url = f"{self.base_link}/find/"
        #https://www.imdb.com/find/?q=Godfather&ref_=nv_sr_sm
        #https://www.imdb.com/find/?q=shawshank%20redemption&ref_=nv_sr_sm
        #https://www.imdb.com/find/?q=shawshank%2520redemption&ref_=nv_sr_sm
        #https://www.imdb.com/find/?q=shawshank+redemption&ref_=nv_sr_sm
        #https://www.imdb.com/find?q=shawshank+redemption&ref_=nv_sr_sm
        params = {"q":self.movie_name, "ref_":"nv_sr_sm"}
        try: 
            response = requests.get(search_url, params=params, timeout=10)
            response.raise_for_status() #checks for response status code and raises error if something wrong
        except requests.RequestException as re:
            log.Error("Error in fetching information for movie: %s, and link: %s", self.movie_name, search_url)
            return None
        soup = BeautifulSoup(response.text, "html.parser")
        result = soup.find("td", class_="result_text")
        #todo encoded string not working , fix it
        




