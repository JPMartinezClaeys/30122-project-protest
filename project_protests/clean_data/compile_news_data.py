import json
import pandas as pd
import os
from .collecting_news import create_dirs
from .clean_data import create_csv
from ..project_protests.api_requests.the_guardian.make_requests import get_json_files
from ..project_protests.api_requests.the_guardian.clean_files import create_news_df
from ..config import the_guardian_api_key

def compile_news_data(collect_data = False):
    """
    Obtain the data from both NYT and The Guardian and compile it into one csv
    
    Inputs:
        collect_data (bool): If True collect_json files, if False skip and move
        on to compilling csv files
    
    Return:
    None - saves a csv that compiles the information of both newspapers
    """

    #Create json files and subdirectories:
    if collect_data:
        create_dirs()
        get_json_files(the_guardian_api_key)

    #Save json files as csv's
    create_csv()
    create_news_df()

    #Compile csv's and save data
    current_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    nyt_df = pd.read_csv(os.path.join(current_dir, "raw_data/nyt_articles.csv"))
    the_guardian_df = pd.read_csv(os.path.join(parent_dir,
    "project_protests/api_requests/the_guardian/data/the_guardian_compiled.csv"))

    the_guardian_df["newspaper"] = "The Guardian"
    nyt_df["newspaper"] = "New York Times"
    nyt_df.rename(columns = {"type_of_material":"type"}, inplace = True)

    news_df = pd.concat([nyt_df,the_guardian_df])

    news_df.to_csv(os.path.join(current_dir, "news_compiled.csv"), index = False)




