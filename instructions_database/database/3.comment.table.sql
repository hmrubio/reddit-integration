-- rubiomatias2_coderhouse."comment" definition

-- Drop table

-- DROP TABLE rubiomatias2_coderhouse."comment";

--DROP TABLE rubiomatias2_coderhouse."comment";
CREATE TABLE IF NOT EXISTS rubiomatias2_coderhouse."comment"
(
	post_id VARCHAR(256) NOT NULL  ENCODE lzo
	,post_id_father VARCHAR(256)   ENCODE lzo
	,subreddit_id VARCHAR(256) NOT NULL  ENCODE lzo
	,title VARCHAR(256)   ENCODE lzo
	,author_id VARCHAR(256)   ENCODE lzo
	,url VARCHAR(256)   ENCODE lzo
	,text VARCHAR(256)   ENCODE lzo
	,PRIMARY KEY (subreddit_id, post_id)
)
DISTSTYLE AUTO
;
ALTER TABLE rubiomatias2_coderhouse."comment" owner to rubiomatias2_coderhouse;


-- rubiomatias2_coderhouse."comment" foreign keys

ALTER TABLE rubiomatias2_coderhouse."comment" ADD CONSTRAINT comment_author_fk FOREIGN KEY (author_id) REFERENCES rubiomatias2_coderhouse.author(author_id);
ALTER TABLE rubiomatias2_coderhouse."comment" ADD CONSTRAINT comment_subreddit_fk FOREIGN KEY (subreddit_id) REFERENCES rubiomatias2_coderhouse.subreddit(subreddit_id);