drop table if exists questions;
create table questions (
  id int unique not null,
  title text not null,
  follower_count int not null,
  answer_count int not null,
  comment_count int not null,
  topic_id int not null
);