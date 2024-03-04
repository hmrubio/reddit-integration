DROP TABLE rubiomatias2_coderhouse.fact_daily_comments_published;
CREATE TABLE IF NOT EXISTS rubiomatias2_coderhouse.fact_daily_comments_published
(
	date DATE NOT NULL  ENCODE az64
	,subreddit_id_most_ocurrences VARCHAR(256) NOT NULL  ENCODE lzo
	,author_id_most_ocurrences VARCHAR(256) NOT NULL  ENCODE lzo
	,amount_comments INTEGER NOT NULL  ENCODE az64
	,user_id VARCHAR(256)   ENCODE lzo
	,update_date TIMESTAMP   ENCODE az64
	,"disable" CHAR(1)   ENCODE lzo
	,PRIMARY KEY (date)
)
DISTSTYLE KEY
 DISTKEY (date)
 SORTKEY (
	date
	)
;

ALTER TABLE rubiomatias2_coderhouse.fact_daily_comments_published ADD CONSTRAINT fact_daily_comments_published_dim_author_fk FOREIGN KEY (author_id_most_ocurrences) REFERENCES rubiomatias2_coderhouse.dim_author(author_id);
ALTER TABLE rubiomatias2_coderhouse.fact_daily_comments_published ADD CONSTRAINT fact_daily_comments_published_dim_subreddit_fk FOREIGN KEY (subreddit_id_most_ocurrences) REFERENCES rubiomatias2_coderhouse.dim_subreddit(subreddit_id);
