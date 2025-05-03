"""Main script to read movie data, clean it, and upload it to Notion."""
import argparse
import asyncio
import time

import pandas as pd

from nuploaders import CONFIG, log
from nuploaders import file_reader, imdb_url_fetcher, notion_client


async def main():
    """Main function to perform create, update or creup operation on Notion database."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action",
        type=str,
        help="Type of action: create, update, or create & update (creup)"
    )
    args = parser.parse_args()

    rdobj = file_reader.ReadActor()
    df_obj = rdobj.read_file(CONFIG["raw_files"]["movies"]["path"])
    df = df_obj.read()
    cleaned_df = await clean_movies_dataframe(df)
    notion_obj = notion_client.NotionDBManager()

    if args.action == "create":
        parent_page_id = CONFIG["notion"]["uploader"]["movies"]["parent_page_id"]
        db_name = CONFIG["notion"]["uploader"]["movies"]["db_name"]
        page_title_icon = CONFIG["notion"]["uploader"]["movies"]["icon"]
        column_name_property = get_col_properties_format()

        notion_obj.create_database(
            parent_page_id=parent_page_id,
            db_name=db_name,
            column_name_property=column_name_property,
            page_title_icon=page_title_icon
        )

    elif args.action == "update":
        update_tasks = []
        for _, row in cleaned_df.iterrows():
            update_tasks.append(notion_obj.write_to_database(row, None))
        await asyncio.gather(*update_tasks)

    elif args.action == "creup":
        parent_page_id = CONFIG["notion"]["uploader"]["movies"]["parent_page_id"]
        db_name = CONFIG["notion"]["uploader"]["movies"]["db_name"]
        page_title_icon = CONFIG["notion"]["uploader"]["movies"]["icon"]
        column_name_property = get_col_properties_format()

        new_db = notion_obj.create_database(
            parent_page_id=parent_page_id,
            db_name=db_name,
            column_name_property=column_name_property,
            page_title_icon=page_title_icon
        )

        cu_tasks = []
        for _, row in cleaned_df.iterrows():
            cu_tasks.append(notion_obj.write_to_database(row, new_db["id"]))
        await asyncio.gather(*cu_tasks)


async def clean_movies_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Unpivots movie dataframe and enriches it with IMDb data."""
    unpivot_df = df.melt(var_name="mycategory", value_name="name")
    unpivot_df = unpivot_df[["name", "mycategory"]]
    unpivot_df = unpivot_df[unpivot_df["name"].notna() & (unpivot_df["name"] != "")]

    omdb_obj = imdb_url_fetcher.OMDBClient(CONFIG["omdb"]["base_link"])
    movie_results = []

    tasks = [
        fetch_and_update(omdb_obj, row, CONFIG["imdb"]["validate"], movie_results)
        for index, row in unpivot_df.iterrows()
    ]
    await asyncio.gather(*tasks)
    return pd.DataFrame(movie_results)


async def fetch_and_update(omdb_obj, row, validate, movie_results):
    """Fetches movie metadata and appends to results."""
    movie_obj = await omdb_obj.fetch_movie(row["name"], row["mycategory"], validate)

    if movie_obj is None:
        log.error("Movie object for %s is None. Skipping...", {row['name']})
        return

    if validate:
        movie_obj.imdblink = await movie_obj.imdblink

    movie_results.append({
        "title": movie_obj.title,
        "runtime": movie_obj.runtime,
        "enrich_mycategory": movie_obj.mycategory,
        "genre": movie_obj.genre,
        "ratings": str(movie_obj.ratings),
        "imdbrating": movie_obj.imdbrating,
        "imdbid": movie_obj.imdbid,
        "imdblink": movie_obj.imdblink,
    })


def get_col_properties_format() -> dict:
    """Formats Notion column property schema from dataframe."""
    return {
        "title": {"type": "string", "col_options": []},
        "runtime": {"type": "string", "col_options": []},
        "enrich_mycategory": {"type": "string", "col_options": []},
        "genre": {"type": "string", "col_options": []},
        "ratings": {"type": "string", "col_options": []},
        "imdbrating": {"type": "string", "col_options": []},
        "imdbid": {"type": "string", "col_options": []},
        "imdblink": {"type": "link", "col_options": []},
    }


if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    elapsed_time = end_time - start_time
    log.warning("Time taken: %s seconds", elapsed_time)
