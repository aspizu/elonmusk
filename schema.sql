CREATE TABLE users (
  id       INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT    NOT NULL UNIQUE,
  email    TEXT    NOT NULL,
  password TEXT    NOT NULL, -- hashed and salted password
  bio      TEXT    NOT NULL,
  pfp      TEXT    NOT NULL, -- URL to profile picture image
  time     INTEGER NOT NULL, -- time of user creation in UNIX time
  role     INTEGER NOT NULL  -- role =  1 -> Admin user
);                           -- role =  0 -> Normal user
                             -- role = -1 -> Hidden user
                             -- role - -2 -> Banned user

CREATE TABLE followers ( -- a row indicates user is followed by follower user
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
  time    INTEGER NOT NULL, -- time of post creation in UNIX time
  visible BOOLEAN NOT NULL,
  FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE post_likes ( -- a row indicates user has either liked or disliked post
  id      INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  post_id INTEGER NOT NULL,
  is_like BOOLEAN NOT NULL, -- true  -> user has liked post
                            -- false -> user has disliked post
  UNIQUE (post_id, user_id),
  FOREIGN KEY(user_id) REFERENCES users(id),
  FOREIGN KEY(post_id) REFERENCES posts(id)
);

CREATE TABLE hashtags ( -- a row indicates the presence of hashtag in post
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
  time    INTEGER NOT NULL, -- time of comment creation in UNIX time
  visible BOOLEAN NOT NULL,
  FOREIGN KEY(user_id) REFERENCES users(id),
  FOREIGN KEY(post_id) REFERENCES posts(id)
);

CREATE TABLE comment_likes ( -- same as post_likes
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id    INTEGER NOT NULL,
  comment_id INTEGER NOT NULL,
  is_like    BOOLEAN NOT NULL, -- same as post_likes.is_like
  UNIQUE (comment_id, user_id),
  FOREIGN KEY(user_id) REFERENCES users(id),
  FOREIGN KEY(comment_id) REFERENCES comments(id)
);
