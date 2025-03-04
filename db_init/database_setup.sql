CREATE TABLE IF NOT EXISTS reddit_msgs (
    id SERIAL PRIMARY KEY,
    comment_id TEXT NOT NULL,
    username TEXT NOT NULL,
    message TEXT NOT NULL,
    num_words INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);