import sqlalchemy as sa
from sqlalchemy.engine.url import URL as Redshift

url = Redshift.create(
    drivername='redshift+redshift_connector',
    host="host",
    port="port",
    database="database",
    username="user",
    password="password",
)

instructions = "CREATE TABLE rubiomatias2_coderhouse.subreddit (" \
    + "subreddit_id varchar NULL," \
    + "user_id varchar NULL," \
    + "update_date time NULL," \
    + '"disable" varchar NULL);' \
    "COMMENT ON TABLE rubiomatias2_coderhouse.subreddit IS 'Subreddits de Reddit';"

engine = sa.create_engine(url)