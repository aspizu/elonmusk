CREATE TABLE users (
  id       INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT    NOT NULL UNIQUE,
  email    TEXT    NOT NULL,
  password TEXT    NOT NULL,
  bio      TEXT    NOT NULL,
  pfp      TEXT    NOT NULL,
  time     INTEGER NOT NULL,
  role     INTEGER NOT NULL
);

CREATE TABLE followers (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  follower_id INTEGER NOT NULL,
  user_id     INTEGER NOT NULL,
  FOREIGN KEY(follower_id) REFERENCES users(id),
  FOREIGN KEY(user_id) REFERENCES users(id),
  UNIQUE (follower_id, user_id)
);

CREATE TABLE posts (
  id      INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  body    TEXT    NOT NULL,
  time    INTEGER NOT NULL,
  visible BOOLEAN NOT NULL,
  FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE post_likes (
  id      INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  post_id INTEGER NOT NULL,
  is_like BOOLEAN NOT NULL,
  UNIQUE (post_id, user_id),
  FOREIGN KEY(user_id) REFERENCES users(id),
  FOREIGN KEY(post_id) REFERENCES posts(id)
);

CREATE TABLE hashtags (
  id      INTEGER PRIMARY KEY AUTOINCREMENT,
  hashtag TEXT    NOT NULL,
  post_id INTEGER NOT NULL,
  UNIQUE (post_id, hashtag),
  FOREIGN KEY(post_id) REFERENCES posts(id)
);

CREATE TABLE comments (
  id      INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  post_id INTEGER NOT NULL,
  body    TEXT    NOT NULL,
  time    INTEGER NOT NULL,
  visible BOOLEAN NOT NULL,
  FOREIGN KEY(user_id) REFERENCES users(id),
  FOREIGN KEY(post_id) REFERENCES posts(id)
);

CREATE TABLE comment_likes (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id    INTEGER NOT NULL,
  comment_id INTEGER NOT NULL,
  is_like    BOOLEAN NOT NULL,
  UNIQUE (comment_id, user_id),
  FOREIGN KEY(user_id) REFERENCES users(id),
  FOREIGN KEY(comment_id) REFERENCES comments(id)
);
