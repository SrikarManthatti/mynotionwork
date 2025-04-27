import pandas as pd
from nuploaders import CONFIG, log
from nuploaders import file_reader, imdb_url_fetcher, notion_client
import argparse
import asyncio

def main():
    #read the data file
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action", 
        type=str, 
        help="Type of action that you want to do create, update, create & update `creup`"
    )
    args = parser.parse_args()
    
    rdobj = file_reader.ReadActor()
    df_obj = rdobj.read_file(CONFIG["raw_files"]["movies"]["path"])
    df = df_obj.read()
    cleaned_df = asyncio.run(clean_movies_dataframe(df))
    notion_obj = notion_client.NotionDBManager()

    #notion db config
    if args.action == "create":
        parent_page_id = CONFIG["notion"]["uploader"]["movies"]["parent_page_id"]
        db_name = CONFIG["notion"]["uploader"]["movies"]["db_name"]
        page_title_icon = CONFIG["notion"]["uploader"]["movies"]["icon"]
        column_name_property = get_col_properties_format(cleaned_df)

        notion_obj.create_database(parent_page_id = parent_page_id, db_name = db_name, column_name_property = column_name_property,  page_title_icon = page_title_icon)
    elif args.action == "update":
        for idx,row in cleaned_df.iterrows():
            notion_obj.write_to_database()
    elif args.action == "creup":
        parent_page_id = CONFIG["notion"]["uploader"]["movies"]["parent_page_id"]
        db_name = CONFIG["notion"]["uploader"]["movies"]["db_name"]
        page_title_icon = CONFIG["notion"]["uploader"]["movies"]["icon"]
        column_name_property = get_col_properties_format(cleaned_df)

        db_name = notion_obj.create_database(parent_page_id = parent_page_id, db_name = db_name, column_name_property = column_name_property,  page_title_icon = page_title_icon)
        for idx,row in cleaned_df.iterrows():
            notion_obj.write_to_database(row, db_name['id'])

async def clean_movies_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """THe sheet which we got have myowncategory as columns so we will change that as a column"""
        #unpivoting the df to make column names as myown category
        unpivot_df = df.melt(var_name='mycategory', value_name='name')
        unpivot_df = unpivot_df[['name', 'mycategory']]

        omdb_obj = imdb_url_fetcher.OMDBClient(CONFIG["omdb"]["base_link"])
        tasks = []
        for index, row in unpivot_df.iterrows():
            tasks.append(fetch_and_update(unpivot_df, omdb_obj, index, row))
        await asyncio.gather(*tasks)
        return unpivot_df

async def fetch_and_update(unpivot_df, omdb_obj, index, row):
        log.info("Info for movie %s", row['name'])
        movie_obj = await omdb_obj.fetch_movie(row['name'], row['mycategory'])
        unpivot_df.loc[index, ['title','runtime','enrich_mycategory','genre','ratings','imdbrating','imdbid','imdblink']] = [
        movie_obj.title,
        movie_obj.runtime,
        movie_obj.mycategory,
        movie_obj.genre,
        str(movie_obj.ratings),
        movie_obj.imdbrating,
        movie_obj.imdbid,
        movie_obj.imdblink
        ]

def get_col_properties_format(df):
    #{"cola":{"type":"string","col_options":[]}}
    new_df = df[['title','runtime','enrich_mycategory','genre','ratings','imdbrating','imdbid','imdblink']]
    property_dict = {}
    property_dict['title'] = {"type":"string", "col_options":[]}
    property_dict['runtime'] = {"type":"string", "col_options":[]}
    property_dict['enrich_mycategory'] = {"type":"string", "col_options":[]}
    property_dict['genre'] = {"type":"string", "col_options":[]}
    property_dict['ratings'] = {"type":"string", "col_options":[]}
    property_dict['imdbrating'] = {"type":"string", "col_options":[]}
    property_dict['imdbid'] = {"type":"string", "col_options":[]}
    property_dict['imdblink'] = {"type":"link", "col_options":[]}
    return property_dict

if __name__=="__main__":
    main()