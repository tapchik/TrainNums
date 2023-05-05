drop table if exists user; 

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