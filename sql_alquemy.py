import sqlalchemy as sa
from sqlalchemy.engine.url import URL

# build the sqlalchemy URL
url = URL.create(
    drivername='redshift+redshift_connector',
    host="host",
    port="port",
    database="database",
    username="user",
    password="password",
)

engine = sa.create_engine(url)