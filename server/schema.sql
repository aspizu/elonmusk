CREATE TABLE users (
  id       INT  PRIMARY KEY,
  username TEXT NOT NULL UNIQUE,
  email    TEXT NOT NULL,
  password TEXT NOT NULL,
  bio      TEXT NOT NULL,
  pfp      TEXT NOT NULL,
  role     INT  NOT NULL
);

CREATE TABLE posts (
  id      INT  PRIMARY KEY,
  user_id INT  NOT NULL,
  body    TEXT NOT NULL,
  time    INT  NOT NULL,
  FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE post_likes (
  id      INT     PRIMARY KEY,
  user_id INT     NOT NULL,
  post_id INT     NOT NULL,
  is_like BOOLEAN NOT NULL,
  UNIQUE (post_id, user_id),
  FOREIGN KEY(user_id) REFERENCES users(id),
  FOREIGN KEY(post_id) REFERENCES posts(id)
);

CREATE TABLE hashtags (
  id      INT  PRIMARY KEY,
  hashtag TEXT NOT NULL,
  post_id INT  NOT NULL,
  UNIQUE (post_id, hashtag),
  FOREIGN KEY(post_id) REFERENCES posts(id)
);

CREATE TABLE comments (
  id      INT  PRIMARY KEY,
  user_id INT  NOT NULL,
  post_id INT  NOT NULL,
  body    TEXT NOT NULL,
  time    INT  NOT NULL
  FOREIGN KEY(user_id) REFERENCES users(id),
  FOREIGN KEY(post_id) REFERENCES posts(id)
);

CREATE TABLE comment_likes (
  id         INT     PRIMARY KEY,
  user_id    INT     NOT NULL,
  comment_id INT     NOT NULL,
  is_like    BOOLEAN NOT NULL,
  UNIQUE (comment_id, user_id),
  FOREIGN KEY(user_id) REFERENCES users(id),
  FOREIGN KEY(comment_id) REFERENCES comments(id)
);
