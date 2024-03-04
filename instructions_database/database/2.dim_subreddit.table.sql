DROP TABLE rubiomatias2_coderhouse.dim_subreddit;
CREATE TABLE IF NOT EXISTS rubiomatias2_coderhouse.dim_subreddit
(
	subreddit_id VARCHAR(256) NOT NULL  ENCODE lzo
	,description VARCHAR(256)   ENCODE lzo
	,user_id VARCHAR(256)   ENCODE lzo
	,update_date TIMESTAMP   ENCODE az64
	,"disable" CHAR(1)   ENCODE lzo
	,PRIMARY KEY (subreddit_id)
)
DISTSTYLE even
SORTKEY(subreddit_id)
;