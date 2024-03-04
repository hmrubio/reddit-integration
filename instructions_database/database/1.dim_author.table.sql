DROP TABLE rubiomatias2_coderhouse.dim_author;
CREATE TABLE IF NOT EXISTS rubiomatias2_coderhouse.dim_author
(
	author_id VARCHAR(256) NOT NULL  ENCODE lzo
	,user_id VARCHAR(256)   ENCODE lzo
	,update_date TIMESTAMP   ENCODE az64
	,"disable" CHAR(1)   ENCODE lzo
	,PRIMARY KEY (author_id)
)
diststyle even
sortkey(author_id)
;