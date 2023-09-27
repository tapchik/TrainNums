PRAGMA foreign_keys = ON;

drop table if exists "user"; 
drop table if exists task;
drop table if exists settings;
drop table if exists statistics;
drop table if exists users;

CREATE TABLE users (
	id text PRIMARY KEY, 
	username text
);

create table task (
	user_id text,
	problem text(45),
	asnwer text(40),
	FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE settings (
	user_id text,
	addition Boolean DEFAULT (1),
	subtraction Boolean DEFAULT (1),
	multiplication Boolean DEFAULT (0),
	division Boolean DEFAULT (0),
	max_sum INTEGER DEFAULT (25),
	max_factor INTEGER DEFAULT (10),
	FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

create table statistics (
	user_id text,
	correct INTEGER DEFAULT (0),
	incorrect INTEGER DEFAULT (0),
	skipped INTEGER DEFAULT (0),
	FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

insert into users (id) values (345);

insert into task values (345, 1, 2);

select * from users;

select * from task;

select * from settings;

select * from statistics;



CREATE TABLE user (
	userid TEXT(30),
	state INTEGER DEFAULT (1),
	problem TEXT(45),
	answer TEXT(40), 
	addition INTEGER DEFAULT (1),
	subtraction INTEGER DEFAULT (1),
	multiplication INTEGER DEFAULT (0),
	division INTEGER DEFAULT (0),
	max_sum INTEGER DEFAULT (25),
	max_factor INTEGER DEFAULT (10),
	correct INTEGER DEFAULT (0),
	incorrect INTEGER DEFAULT (0),
	skipped INTEGER DEFAULT (0)
);