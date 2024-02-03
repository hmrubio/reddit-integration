CREATE TABLE RedditData (
    post_id VARCHAR(255) PRIMARY KEY,
    subreddit VARCHAR(255),
    title VARCHAR(255),
    ups INT,
    num_comments INT,
    author VARCHAR(255),
    created_utc FLOAT,
    stickied BOOLEAN,
    url VARCHAR(255),
    subreddit_subscribers INT,
    is_video BOOLEAN,
    body TEXT,
    permalink VARCHAR(255)
);
