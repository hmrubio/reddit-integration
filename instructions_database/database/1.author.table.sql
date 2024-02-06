-- rubiomatias2_coderhouse.author definition

-- Drop table

-- DROP TABLE rubiomatias2_coderhouse.author;

--DROP TABLE rubiomatias2_coderhouse.author;
CREATE TABLE IF NOT EXISTS rubiomatias2_coderhouse.author
(
	author_id VARCHAR(256) NOT NULL  ENCODE lzo
	,user_id VARCHAR(256)   ENCODE lzo
	,update_date VARCHAR(256)   ENCODE lzo
	,"disable" VARCHAR(256)   ENCODE lzo
	,PRIMARY KEY (author_id)
)
DISTSTYLE AUTO
;
ALTER TABLE rubiomatias2_coderhouse.author owner to rubiomatias2_coderhouse;