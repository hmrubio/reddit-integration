import json
import os
from datetime import datetime

import pandas
import sqlalchemy
import configparser

from pandas import DataFrame
from sqlalchemy.engine.url import URL

config_file_parser = configparser.ConfigParser()
config_file_parser.read('redshift_database.py.ini')

general_config = config_file_parser['GENERAL']
data_files_config = config_file_parser['DATA_FILES']

host = general_config["HOST"]
port = general_config.getint("PORT")
database = general_config["DATABASE"]
username = general_config["USER"]
password = general_config["PASS"]
schema = general_config['SCHEMA']

user_id = "admin"
update_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
disable = "N"


def deep_search_recursive(children: list, info_dict: dict):
    for value in children:
        comment: dict = value["data"]

        comment_body: str = comment["body"] if "body" in comment else ""
        comment_id: str = f"{value['kind']}_{comment['id']}"
        comment_parent_id: str = comment["parent_id"] if "parent_id" in comment else ""
        comment_subreddit_id: str = comment["subreddit_id"] if "subreddit_id" in comment else ""
        comment_title: str = comment["title"] if "title" in comment else ""
        comment_url: str = comment["permalink"] if "permalink" in comment else ""

        author_id: str = comment["author"] if "author" in comment else ""

        subreddit_id: str = comment["subreddit_id"] if "subreddit_id" in comment else ""
        subreddit_name_prefixed: str = comment["subreddit_name_prefixed"] if "subreddit_name_prefixed" in comment else ""

        comment_dict = {
            "text": comment_body,
            "post_id": comment_id,
            "post_id_father": comment_parent_id,
            "subreddit_id": comment_subreddit_id,
            "title": comment_title,
            "url": comment_url,
            "author_id": author_id,
            "user_id": user_id,
            "update_date": update_date,
            "disable": disable
        }

        author_dict = {
            "author_id": author_id,
            "user_id": user_id,
            "update_date": update_date,
            "disable": disable
        }

        subreddit_dict = {
            "subreddit_id": subreddit_id,
            "description": subreddit_name_prefixed,
            "user_id": user_id,
            "update_date": update_date,
            "disable": disable
        }

        info_dict.setdefault("comments", list()).append(comment_dict)

        authors = info_dict.setdefault("authors", list())
        if author_dict not in authors:
            authors.append(author_dict)

        subreddits = info_dict.setdefault("subreddits", list())
        if subreddit_dict not in subreddits:
            subreddits.append(subreddit_dict)

        if "replies" in comment:
            if "data" in comment["replies"]:
                deep_search_recursive(comment["replies"]["data"]["children"], info_dict)


def insert_into_database(table: str, dataframe: DataFrame):
    url = URL.create(
        drivername='redshift+redshift_connector',
        host=host,
        port=port,
        database=database,
        username=username,
        password=password,
    )

    engine = sqlalchemy.create_engine(url)
    with engine.connect() as conn:
        dataframe.to_sql(table, conn,
                         schema="rubiomatias2_coderhouse",
                         if_exists="append",
                         method=None,
                         chunksize=1000,
                         index=False)


directory = data_files_config["PATH"]
files = os.listdir(directory)
for file in files:
    path = f"{directory}/{file}"
    print(path)

    with open(path) as file:
        dictionary: list = json.load(file)

    replies = dictionary.pop()
    main_comment = dictionary.pop()
    info_dict: dict = {
        "authors": list(),
        "comments": list(),
        "subreddits": list()
    }

    deep_search_recursive(main_comment["data"]["children"], info_dict)
    deep_search_recursive(replies["data"]["children"], info_dict)

    dataframe_authors = pandas.json_normalize(info_dict, ["authors"])
    dataframe_comments = pandas.json_normalize(info_dict, ["comments"])
    dataframe_subreddits = pandas.json_normalize(info_dict, ["subreddits"])

    try:
        insert_into_database("dim_author", dataframe_authors)
        insert_into_database("dim_comment", dataframe_comments)
        insert_into_database("dim_subreddit", dataframe_subreddits)
    except:
        print("There was a problem. Continuing with next file...")
        continue

    print("Finished.\n")