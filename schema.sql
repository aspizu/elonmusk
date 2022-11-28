create table users (
  id       integer primary key autoincrement, 
  username text not null unique,
  email    text not null,
  password text not null,
  avatar   text not null,
  bio      text not null,
  time     integer not null,
  rank     integer not null
);


create table followers (
  id          integer primary key autoincrement,
  follower_id integer not null,
  user_id     integer not null,
  unique (follower_id, user_id),
  foreign key(follower_id) references users(id),
  foreign key(user_id) references users(id)
);


create table posts (
  id      integer primary key autoincrement,
  user_id integer not null,
  body    text not null,
  time    integer not null,
  foreign key(user_id) references users(id)
);


create table post_likes (
  id      integer primary key autoincrement,
  user_id integer not null,
  post_id integer not null,
  unique (post_id, user_id),
  foreign key(user_id) references users(id),
  foreign key(post_id) references posts(id)
);


create table comments (
  id      integer primary key autoincrement,
  user_id integer not null,
  post_id integer not null,
  body    text not null,
  time    integer not null,
  foreign key(user_id) references users(id),
  foreign key(post_id) references posts(id)
);


create table comment_likes (
  id         integer primary key autoincrement,
  user_id    integer not null,
  comment_id integer not null,
  unique (comment_id, user_id),
  foreign key(user_id) references users(id),
  foreign key(comment_id) references comments(id)
);


create table transactions (
  id      integer primary key autoincrement,
  from_id integer not null,
  to_id   integer not null,
  amount integer not null,
  foreign key(from_id) references users(id),
  foreign key(to_id) references users(id)
)
