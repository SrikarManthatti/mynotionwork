import pandas as pd
from nuploaders import CONFIG
from nuploaders import file_reader, imdb_url_fetcher, notion_client

def main():
    #read the data file
    rdobj = ReadActor()
    df = rdobj.read_file(CONFIG["raw_files"]["movies"]["path"])
    print("just priting testing")
    print(df.shape)


