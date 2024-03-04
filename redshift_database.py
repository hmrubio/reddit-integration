import json
import pandas
import sqlalchemy
import configparser
from sqlalchemy.engine.url import URL


config_file_parser = configparser.ConfigParser()
config_file_parser.read('redshift_database.py.ini')

general_config = config_file_parser['GENERAL']

host=general_config["HOST"]
port=general_config.getint("PORT")
database=general_config["DATABASE"]
username=general_config["USER"]
password=general_config["PASS"]
schema = general_config['SCHEMA']

url = URL.create(
    drivername='redshift+redshift_connector',
    host=host,
    port=port,
    database=database,
    username=username,
    password=password,
)

#engine = sqlalchemy.create_engine(
#    f"redshift+psycopg2://{username}:{password}@{host}:{port}/{database}"
#)

engine = sqlalchemy.create_engine(url)

with open("C:/Users/hmr/OneDrive - Penta Consulting S.A/Estudio/Ingeniería de Datos/Proyecto final/data/comments/AirsoftEnArgentina_1922vhy.json") as file:
    dictionary = json.load(file)

#print(dictionary)

path = "C:/Users/hmr/OneDrive - Penta Consulting S.A/Estudio/Ingeniería de Datos/Proyecto final/data/comments/AirsoftEnArgentina_1922vhy.json"
#dataframe_json = pandas.read_json(path)

dataframe_json = pandas.json_normalize(dictionary, ["data", "children"])["data.author"].head()

#dataframe_json = pandas.DataFrame(dictionary)
print(dataframe_json)

dataframe_json.to_sql(f"dim_author", engine.connect(),
            schema="rubiomatias2_coderhouse",
            if_exists="append",
            method="multi",
            chunksize=1000,
            index=False)

#print(dataframe_json["data.subreddit"])
