DROP TABLE rubiomatias2_coderhouse.dim_comment;
CREATE TABLE IF NOT EXISTS rubiomatias2_coderhouse.dim_comment
(
	subreddit_id VARCHAR(256) NOT NULL  ENCODE lzo
	,post_id VARCHAR(256) NOT NULL  ENCODE lzo
	,post_id_father VARCHAR(256)   ENCODE lzo
	,title VARCHAR(256)   ENCODE lzo
	,author_id VARCHAR(256)   ENCODE lzo
	,url VARCHAR(256)   ENCODE lzo
	,text VARCHAR(20000)   ENCODE lzo
	,user_id VARCHAR(256)   ENCODE lzo
	,update_date TIMESTAMP   ENCODE az64
	,"disable" CHAR(1)   ENCODE lzo
	,PRIMARY KEY (subreddit_id, post_id)
)
DISTKEY(subreddit_id)
SORTKEY(subreddit_id, post_id)
;

ALTER TABLE rubiomatias2_coderhouse.dim_comment ADD CONSTRAINT dim_comment_dim_author_fk FOREIGN KEY (author_id) REFERENCES rubiomatias2_coderhouse.dim_author(author_id);
ALTER TABLE rubiomatias2_coderhouse.dim_comment ADD CONSTRAINT dim_comment_dim_subreddit_fk FOREIGN KEY (subreddit_id) REFERENCES rubiomatias2_coderhouse.dim_subreddit(subreddit_id);
