drop table if exists questions;
create table questions (
  id int unique not null,
  title text not null,
  follower_count int not null,
  answer_count int not null,
  comment_count int not null,
  topic_id int not null
);

drop table if exists answers;
create table questions (
  id int unique not null,
  follower_count int not null,
  voteup_count int not null,
  thanks_count int not null,
  question_id int not null
);