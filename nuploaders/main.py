import pandas as pd
from nuploaders import CONFIG, log
from nuploaders import file_reader, imdb_url_fetcher, notion_client

def main():
    #read the data file
    rdobj = file_reader.ReadActor()
    df_obj = rdobj.read_file(CONFIG["raw_files"]["movies"]["path"])
    df = df_obj.read()

    cleaned_df = clean_movies_dataframe(df)
    cleaned_df.to_csv("output.csv")
    log.info(cleaned_df)

def clean_movies_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """THe sheet which we got have myowncategory as columns so we will change that as a column"""
    #unpivoting the df to make column names as myown category
    unpivot_df = df.melt(var_name='mycategory', value_name='name')
    unpivot_df = unpivot_df[['name', 'mycategory']]

    omdb_obj = imdb_url_fetcher.OMDBClient(CONFIG["omdb"]["base_link"])
    for index, row in unpivot_df.iterrows():
        log.info("Info for movie %s", row['name'])
        movie_obj = omdb_obj.fetch_movie(row['name'], row['mycategory'])
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
    return unpivot_df


if __name__=="__main__":
    main()