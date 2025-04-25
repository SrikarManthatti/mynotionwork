import pandas as pd
from nuploaders import CONFIG, log
from nuploaders import file_reader, imdb_url_fetcher, notion_client

def main():
    #read the data file
    rdobj = file_reader.ReadActor()
    df_obj = rdobj.read_file(CONFIG["raw_files"]["movies"]["path"])
    df = df_obj.read()
    log.info("just priting testing")
    log.info(df.head())

if __name__ == "__main__":
    main()

