"""Module for fetching IMDB movie data and validating URLs via OMDB and IMDB APIs."""

import os
from typing import Optional
from dataclasses import dataclass

import httpx # pylint: disable=import-error

from nuploaders import CONFIG, log


class IMDBFetcher:
    """Class to generate and optionally validate IMDB URLs for given title IDs."""

    def __init__(self, base_link: str):
        self.base_link = base_link
        self.headers = {'User-Agent': 'Mozilla/5.0'}  # Prevent IMDB 403 errors
        self.ref = "?ref_=fn_all_ttl_1"

    async def generate_link(self, titleid: str, validate_movie_links: bool) -> str:
        """Generate and optionally validate the IMDB link for a movie."""
        log.info("Validating URL for titleid: %s", titleid)
        if validate_movie_links:
            # TODO: Add delay to avoid IMDB blocking IP due to aggressive requests
            return await self._validate_imdb_url(f"{self.base_link}/title/{titleid}/{self.ref}")
        return f"{self.base_link}/title/{titleid}/{self.ref}"

    async def _validate_imdb_url(self, link: str) -> str:
        """Send a GET request to verify the IMDB link."""
        async with httpx.AsyncClient() as client:
            response = await client.get(link, headers=self.headers)
            response.raise_for_status()
        return link


@dataclass
class Movie:
    """Data structure representing a movie."""
    title: str
    runtime: str
    mycategory: str
    genre: str
    ratings: list
    imdbrating: float
    imdbid: str
    imdblink: str


class OMDBClient:
    """Client to fetch movie metadata from the OMDB API."""

    def __init__(self, base_link: str):
        self.api_key = os.getenv("OMDB_API_KEY")
        self.base_link = base_link

    async def fetch_movie(
        self, movie_name: str, mycategory: str, validate: bool
    ) -> Optional[Movie]:
        """Fetch movie metadata and construct a Movie object."""
        params = {"t": movie_name, "apikey": self.api_key}
        try:
            async with httpx.AsyncClient() as asycclient:
                response = await asycclient.get(self.base_link, params=params, timeout=10)
                log.info("Response received for movie %s", movie_name)
            response.raise_for_status()
        except httpx.RequestError:
            log.error("Error in fetching information for movie: %s", movie_name)
            return None

        data = response.json()
        imdb_obj = IMDBFetcher(CONFIG["imdb"]["base_link"])
        validated_movie = await imdb_obj.generate_link(data.get("imdbID", "N/A"), validate)

        if data.get("Response") == "True":
            return Movie(
                title=data.get("Title", "N/A"),
                runtime=data.get("Runtime", "N/A"),
                mycategory=mycategory,
                genre=data.get("Genre", "N/A"),
                ratings=data.get("Ratings", []),
                imdbrating=data.get("imdbRating", "N/A"),
                imdbid=data.get("imdbID", "N/A"),
                imdblink=validated_movie,
            )
        return None
