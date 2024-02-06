-- rubiomatias2_coderhouse.subreddit definition

-- Drop table

-- DROP TABLE rubiomatias2_coderhouse.subreddit;

--DROP TABLE rubiomatias2_coderhouse.subreddit;
CREATE TABLE IF NOT EXISTS rubiomatias2_coderhouse.subreddit
(
	subreddit_id VARCHAR(256) NOT NULL  ENCODE lzo
	,description VARCHAR(256)   ENCODE lzo
	,user_id VARCHAR(256)   ENCODE lzo
	,update_date TIME WITHOUT TIME ZONE   ENCODE az64
	,"disable" BOOLEAN   ENCODE RAW
	,PRIMARY KEY (subreddit_id)
)
DISTSTYLE AUTO
;
ALTER TABLE rubiomatias2_coderhouse.subreddit owner to rubiomatias2_coderhouse;