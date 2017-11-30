DROP DATABASE IF EXISTS MOM_GAME;
CREATE DATABASE MOM_GAME;
USE MOM_GAME;

CREATE TABLE ERROR (message TEXT NOT NULL);
INSERT INTO ERROR VALUES ("Default message");

CREATE TABLE TWO_PART_WORDS (
	word_1 VARCHAR(200) NOT NULL,
	word_2 VARCHAR(200) NOT NULL
);

CREATE TABLE DIRECTION (
	direction_id	VARCHAR (10) NOT NULL,
	name			VARCHAR (40) NOT NULL,
	
	PRIMARY KEY (direction_id)
);

CREATE TABLE ROOM (
	room_id		INT NOT NULL,
	name		VARCHAR (40) NOT NULL,
	description	TEXT, 
	
	PRIMARY KEY (room_id)
);

CREATE TABLE PASSAGE (
	from_id 	INT NOT NULL,
	to_id 		INT NOT NULL,
	direction 	VARCHAR (10) NOT NULL,
	
	PRIMARY KEY (from_id, to_id),
	
	FOREIGN KEY (from_id) 	REFERENCES ROOM(room_id),
	FOREIGN KEY (to_id) 	REFERENCES ROOM(room_id)
);

CREATE TABLE DETAIL (
	detail_id 	INT NOT NULL,
	name 		VARCHAR (40) NOT NULL,
	description TEXT,

	PRIMARY KEY (detail_id)
);

CREATE TABLE NPC (
	npc_id 		INT NOT NULL,
	first_name 	VARCHAR (40) NOT NULL,
	last_name 	VARCHAR (40) NOT NULL,
	description	TEXT,

	map_group	ENUM ('A', 'B') NOT NULL,
	sub_group	INT NOT NULL,
	
	PRIMARY KEY (npc_id)
);
CREATE UNIQUE INDEX MOM_GAME ON NPC (first_name, last_name);

CREATE TABLE NPC_DETAIL (
	npc 	INT NOT NULL,
	detail 	INT NOT NULL,
	
	PRIMARY KEY (npc, detail),
	
	FOREIGN KEY (npc) 		REFERENCES NPC(npc_id),
	FOREIGN KEY (detail) 	REFERENCES DETAIL (detail_id)
);

/*
There will be a intricate set of rules as how to map NPC table to MAPPED NPC.
This will be handled in Python.
*/

CREATE TABLE MAPPED_NPC (
	mapped_id	INT NOT NULL,
	npc 		INT NOT NULL,
	location	INT NOT NULL,
	state 		ENUM (
					'not murderer',
					'murdering',
					'arrested',
					'escaped'
				) NOT NULL,
	
	PRIMARY KEY (mapped_id),
	
	FOREIGN KEY (npc)		REFERENCES NPC (npc_id),
	FOREIGN KEY (location)	REFERENCES ROOM (room_id)
);
CREATE UNIQUE INDEX MOM_GAME ON MAPPED_NPC (npc);

CREATE TABLE MURDER (
	victim 		INT NOT NULL,
	murderer 	INT NOT NULL,
	solved		BOOLEAN NOT NULL,

	PRIMARY KEY (victim),
	
	FOREIGN KEY (victim) 	REFERENCES MAPPED_NPC (mapped_id),
	FOREIGN KEY (murderer) 	REFERENCES MAPPED_NPC (mapped_id)
);

CREATE TABLE CLUE (
	clue_id 	INT NOT NULL AUTO_INCREMENT,
	victim 		INT NOT NULL,
	witness		INT NOT NULL,
	detail 		INT NOT NULL,

	PRIMARY KEY (clue_id),
	
	FOREIGN KEY (victim) 	REFERENCES MURDER (victim),
	FOREIGN KEY (witness) 	REFERENCES MAPPED_NPC (mapped_id),
	FOREIGN KEY (detail) 	REFERENCES DETAIL (detail_id)

);
CREATE UNIQUE INDEX MOM_GAME ON CLUE (victim, witness, 	detail);

CREATE TABLE PLAYER_CLUE (
	victim INT NOT NULL,
	detail INT NOT NULL,

	PRIMARY KEY (victim, detail),

	FOREIGN KEY (victim) REFERENCES MURDER (victim),
	FOREIGN KEY (detail) REFERENCES DETAIL (detail_id)
);

INSERT INTO DIRECTION VALUES ('n', 'north');
INSERT INTO DIRECTION VALUES ('ne', 'northeast');
INSERT INTO DIRECTION VALUES ('e', 'east');
INSERT INTO DIRECTION VALUES ('se', 'southeast');
INSERT INTO DIRECTION VALUES ('s', 'south');
INSERT INTO DIRECTION VALUES ('sw', 'southwest');
INSERT INTO DIRECTION VALUES ('w', 'west');
INSERT INTO DIRECTION VALUES ('nw', 'northwest');
INSERT INTO DIRECTION VALUES ('u', 'up');
INSERT INTO DIRECTION VALUES ('d', 'down');

INSERT INTO room VALUES (1, 'front yard', NULL);
INSERT INTO two_part_words VALUES ('front', 'yard');
INSERT INTO room VALUES (2, 'entrance', NULL);
INSERT INTO room VALUES (3, 'tea room', NULL);
INSERT INTO two_part_words VALUES ('tea', 'room');
INSERT INTO room VALUES (4, 'dining', NULL);
INSERT INTO room VALUES (5, 'bar', NULL);
INSERT INTO room VALUES (6, 'kitchen', NULL);
INSERT INTO room VALUES (7, 'billiard room', NULL);
INSERT INTO two_part_words VALUES ('billiard', 'room');
INSERT INTO room VALUES (8, 'hall', NULL);
INSERT INTO room VALUES (9, 'butlers room', NULL);
INSERT INTO two_part_words VALUES ('butlers', 'room');
INSERT INTO room VALUES (10, 'music room', NULL);
INSERT INTO two_part_words VALUES ('music', 'room');
INSERT INTO room VALUES (11, 'ballroom', NULL);
INSERT INTO room VALUES (12, 'terrace', NULL);
INSERT INTO room VALUES (13, 'gallery', NULL);
INSERT INTO room VALUES (14, 'servants', NULL);
INSERT INTO room VALUES (15, 'bathroom', NULL);
INSERT INTO room VALUES (16, 'kitchen maids', NULL);
INSERT INTO two_part_words VALUES ('kitchen', 'maids');
INSERT INTO room VALUES (17, 'back yard', NULL);
INSERT INTO two_part_words VALUES ('back', 'yard');


-- front yard
INSERT INTO passage VALUES (1, 2, 'n');
-- entrance
INSERT INTO passage VALUES (2, 1, 's');
INSERT INTO passage VALUES (2, 3, 'e');
INSERT INTO passage VALUES (2, 8, 'w');
-- tea room
INSERT INTO passage VALUES (3, 2, 'w');
INSERT INTO passage VALUES (3, 4, 'n');
INSERT INTO passage VALUES (3, 7, 'se');
-- dining
INSERT INTO passage VALUES (4, 3, 's');
INSERT INTO passage VALUES (4, 5, 'w');
-- bar
INSERT INTO passage VALUES (5, 4, 'e');
INSERT INTO passage VALUES (5, 6, 'n');
-- kitchen
INSERT INTO passage VALUES (6, 5, 's');
-- billiard room
INSERT INTO passage VALUES (7, 3, 'nw');
-- hall
INSERT INTO passage VALUES (8, 2, 'e');
INSERT INTO passage VALUES (8, 9, 's');
INSERT INTO passage VALUES (8, 10, 'n');
-- butlers room
INSERT INTO passage VALUES (9, 8, 'n');
-- music room
INSERT INTO passage VALUES (10, 8, 's');
INSERT INTO passage VALUES (10, 11, 'w');
-- ballroom
INSERT INTO passage VALUES (11, 10, 'e');
INSERT INTO passage VALUES (11, 12, 's');
INSERT INTO passage VALUES (11, 13, 'w');
-- terrace
INSERT INTO passage VALUES (12, 11, 'n');
-- gallery
INSERT INTO passage VALUES (13, 11, 'e');
INSERT INTO passage VALUES (13, 14, 's');
-- servants
INSERT INTO passage VALUES (14, 13, 'n');
INSERT INTO passage VALUES (14, 15, 'w');
-- bathroom
INSERT INTO passage VALUES (15, 14, 'e');
INSERT INTO passage VALUES (15, 16, 'n');
-- kitchen maids
INSERT INTO passage VALUES (16, 15, 's');
INSERT INTO passage VALUES (16, 17, 'n');
-- back yard
INSERT INTO passage VALUES (17, 16, 's');


/*
Get room names and directions:
SELECT F.name, T.name, D.name
FROM PASSAGE 
	INNER JOIN ROOM AS F
		ON F.room_id = PASSAGE.from_id
	
	INNER JOIN ROOM AS T
		ON T.room_id = PASSAGE.to_id
	
	INNER JOIN DIRECTION AS D
		ON D.direction_id = PASSAGE.direction;
*/

INSERT INTO DETAIL VALUES (1, 'pocket watch', NULL);
INSERT INTO DETAIL VALUES (2, 'red scarf', NULL);
INSERT INTO DETAIL VALUES (3, 'duck-headed cane', NULL);
INSERT INTO DETAIL VALUES (4, 'flower of clove', NULL);
INSERT INTO DETAIL VALUES (5, 'hat with feathers', NULL);
INSERT INTO DETAIL VALUES (6, 'thick moustache', NULL);
INSERT INTO DETAIL VALUES (7, 'some sauce on their clothes', NULL);
INSERT INTO DETAIL VALUES (8, 'pearl necklace', NULL);
INSERT INTO DETAIL VALUES (9, 'lace collar', null);
INSERT INTO DETAIL VALUES (10, 'flashy earrings', null);
INSERT INTO DETAIL VALUES (11, 'pompous cravat', NULL);
INSERT INTO DETAIL VALUES (12, 'extravagant monocle', NULL);
INSERT INTO DETAIL VALUES (13, 'bulging manhood', NULL);
INSERT INTO DETAIL VALUES (14, 'wine glass in pocket', null);

INSERT INTO NPC VALUES (1, "snorkeldink", "crumplehorn", NULL, 'A', 1);
INSERT INTO NPC VALUES (2, "brewery", "chickenbroth", NULL, 'A', 1);
INSERT INTO NPC VALUES (3, "rinkydink", "chuckecheese", NULL, 'A', 2);
INSERT INTO NPC VALUES (4, "brandenburg", "creamsicle", NULL, 'A', 2);
INSERT INTO NPC VALUES (5, "benadryl", "moldyspore", NULL, 'B', 1);
INSERT INTO NPC VALUES (6, "bumberstump", "cumbercooch", NULL,'B', 1);
INSERT INTO NPC VALUES (7, "benetton", "camouflage", NULL, 'B', 2);
INSERT INTO NPC VALUES (8, "bentobox", "cottagecheese", NULL, 'B', 2);

INSERT INTO NPC_DETAIL VALUES (1, 1);
INSERT INTO NPC_DETAIL VALUES (1, 4);
INSERT INTO NPC_DETAIL VALUES (1, 5);
INSERT INTO NPC_DETAIL VALUES (1, 9);
INSERT INTO NPC_DETAIL VALUES (1, 10);
INSERT INTO NPC_DETAIL VALUES (2, 3);
INSERT INTO NPC_DETAIL VALUES (2, 5);
INSERT INTO NPC_DETAIL VALUES (2, 6);
INSERT INTO NPC_DETAIL VALUES (2, 8);
INSERT INTO NPC_DETAIL VALUES (2, 10);
INSERT INTO NPC_DETAIL VALUES (3, 2);
INSERT INTO NPC_DETAIL VALUES (3, 3);
INSERT INTO NPC_DETAIL VALUES (3, 4);
INSERT INTO NPC_DETAIL VALUES (3, 7);
INSERT INTO NPC_DETAIL VALUES (3, 10);
INSERT INTO NPC_DETAIL VALUES (4, 1);
INSERT INTO NPC_DETAIL VALUES (4, 4);
INSERT INTO NPC_DETAIL VALUES (4, 5);
INSERT INTO NPC_DETAIL VALUES (4, 7);
INSERT INTO NPC_DETAIL VALUES (4, 9);
INSERT INTO NPC_DETAIL VALUES (5, 1);
INSERT INTO NPC_DETAIL VALUES (5, 3);
INSERT INTO NPC_DETAIL VALUES (5, 4);
INSERT INTO NPC_DETAIL VALUES (5, 6);
INSERT INTO NPC_DETAIL VALUES (5, 7);
INSERT INTO NPC_DETAIL VALUES (6, 2);
INSERT INTO NPC_DETAIL VALUES (6, 3);
INSERT INTO NPC_DETAIL VALUES (6, 4);
INSERT INTO NPC_DETAIL VALUES (6, 8);
INSERT INTO NPC_DETAIL VALUES (6, 10);
INSERT INTO NPC_DETAIL VALUES (7, 3);
INSERT INTO NPC_DETAIL VALUES (7, 5);
INSERT INTO NPC_DETAIL VALUES (7, 6);
INSERT INTO NPC_DETAIL VALUES (7, 7);
INSERT INTO NPC_DETAIL VALUES (7, 9);
INSERT INTO NPC_DETAIL VALUES (8, 4);
INSERT INTO NPC_DETAIL VALUES (8, 5);
INSERT INTO NPC_DETAIL VALUES (8, 6);
INSERT INTO NPC_DETAIL VALUES (8, 9);
INSERT INTO NPC_DETAIL VALUES (8, 10);

INSERT INTO MAPPED_NPC VALUES (1, 7, 1, 'not murderer');
INSERT INTO MAPPED_NPC VALUES (2, 6, 1, 'murdering');
INSERT INTO MAPPED_NPC VALUES (3, 4, 1, 'not murderer');
INSERT INTO MAPPED_NPC VALUES (4, 5, 1, 'murdering');
INSERT INTO MAPPED_NPC VALUES (5, 2, 1, 'not murderer');
INSERT INTO MAPPED_NPC VALUES (6, 3, 1, 'arrested');
INSERT INTO MAPPED_NPC VALUES (7, 1, 1, 'escaped');
INSERT INTO MAPPED_NPC VALUES (8, 8, 1, 'not murderer');

INSERT INTO MURDER VALUES (3, 4, False);
INSERT INTO MURDER VALUES (8, 4, False);
INSERT INTO MURDER VALUES (7, 5, True);

INSERT INTO CLUE VALUES (null, 3, 1, 1);
INSERT INTO CLUE VALUES (null, 3, 5, 2);
INSERT INTO CLUE VALUES (null, 3, 2, 3);
INSERT INTO CLUE VALUES (null, 8, 1, 5);
INSERT INTO CLUE VALUES (null, 8, 7, 4);


/*
Clues that person W(itness) knows about killer of V(ictim)
SELECT DETAIL.name
FROM CLUE
	
	INNER JOIN MAPPED_NPC as M_W
		ON M_W.mapped_id = CLUE.witness
		INNER JOIN NPC as W
			ON W.npc_id = M_W.npc
	
	INNER JOIN MURDER
		ON MURDER.murder_id = CLUE.murder
		INNER JOIN MAPPED_NPC as M_V
			ON M_V.mapped_id = MURDER.victim
			INNER JOIN NPC as V
				ON V.npc_id = M_V.npc

	INNER JOIN DETAIL
		ON DETAIL.detail_id = CLUE.detail

WHERE
	V.last_name = "[Victims last name]" AND
	W.last_name = "[Witness' last name]";
	
*/

-- parser section
CREATE TABLE VERB (
	word VARCHAR(100),
	PRIMARY KEY (word)
);

CREATE TABLE PREPOSITIONS (
	word VARCHAR(100) NOT NULL,
	PRIMARY KEY (word)
);

CREATE TABLE ACTIONS (
	id INT NOT NULL,
	verb VARCHAR(100) NOT NULL,
	has_target1 BOOLEAN NOT NULL,
	preposition VARCHAR(100),
	has_target2 BOOLEAN NOT NULL,
	FOREIGN KEY (verb) REFERENCES VERB (word),
	FOREIGN KEY (preposition) REFERENCES PREPOSITIONS(word)
);

CREATE TABLE synonyms (
	word VARCHAR (100) NOT NULL,
	main_word VARCHAR (100) NOT NULL
);

INSERT INTO VERB VALUES ('look');
INSERT INTO VERB VALUES ('move');
INSERT INTO VERB VALUES ('ask');
INSERT INTO VERB VALUES ('blame');

INSERT INTO PREPOSITIONS VALUES ('to');
INSERT INTO PREPOSITIONS VALUES ('at');
INSERT INTO PREPOSITIONS VALUES ('about');
INSERT INTO PREPOSITIONS VALUES ('for');
INSERT INTO PREPOSITIONS VALUES ('from');
INSERT INTO PREPOSITIONS VALUES ('in');
INSERT INTO PREPOSITIONS VALUES ('into');
INSERT INTO PREPOSITIONS VALUES ('like');
INSERT INTO PREPOSITIONS VALUES ('of');
INSERT INTO PREPOSITIONS VALUES ('off');
INSERT INTO PREPOSITIONS VALUES ('on');
INSERT INTO PREPOSITIONS VALUES ('over');
INSERT INTO PREPOSITIONS VALUES ('since');
INSERT INTO PREPOSITIONS VALUES ('than');
INSERT INTO PREPOSITIONS VALUES ('till');
INSERT INTO PREPOSITIONS VALUES ('until');
INSERT INTO PREPOSITIONS VALUES ('via');
INSERT INTO PREPOSITIONS VALUES ('with');
INSERT INTO PREPOSITIONS VALUES ('within');
INSERT INTO PREPOSITIONS VALUES ('without');
INSERT INTO PREPOSITIONS VALUES ('around');
INSERT INTO PREPOSITIONS VALUES ('for killing');
INSERT INTO TWO_PART_WORDS VALUES ('for', 'killing');

INSERT INTO ACTIONS VALUES (10, 'move', False, 'to', True);
INSERT INTO ACTIONS VALUES (11, 'move', False, NULL, True);
INSERT INTO ACTIONS VALUES (20, 'look', False, 'at', True);
INSERT INTO ACTIONS VALUES (21, 'look', False, 'around', False);
INSERT INTO ACTIONS VALUES (21, 'look', False, NULL, FALSE);
INSERT INTO ACTIONS VALUES (30, 'ask', True, 'about', True);
INSERT INTO ACTIONS VALUES (40, 'blame', True, 'for killing', True);

-- VERBS
INSERT INTO synonyms VALUES ('accuse',    'blame');
INSERT INTO synonyms VALUES ('prosecute', 'blame');
INSERT INTO synonyms VALUES ('indict',    'blame');
INSERT INTO synonyms VALUES ('arraign',   'blame');

INSERT INTO synonyms VALUES ('inquire',     'ask');
INSERT INTO synonyms VALUES ('question',    'ask');
INSERT INTO synonyms VALUES ('interrogate', 'ask');

INSERT INTO synonyms VALUES ('eye',     'look');
INSERT INTO synonyms VALUES ('glance',  'look');
INSERT INTO synonyms VALUES ('glimpse', 'look');
INSERT INTO synonyms VALUES ('peek',    'look');
INSERT INTO synonyms VALUES ('view',    'look');
INSERT INTO synonyms VALUES ('gander',  'look');
INSERT INTO synonyms VALUES ('gaze',    'look');
INSERT INTO synonyms VALUES ('inspect', 'look');
INSERT INTO synonyms VALUES ('leer',    'look');
INSERT INTO synonyms VALUES ('observe', 'look');
INSERT INTO synonyms VALUES ('watch',   'look');
INSERT INTO synonyms VALUES ('examine', 'look');
INSERT INTO synonyms VALUES ('see',     'look');

INSERT INTO synonyms VALUES ('go',     'move');
INSERT INTO synonyms VALUES ('walk',   'move');
INSERT INTO synonyms VALUES ('run',    'move');
INSERT INTO synonyms VALUES ('jog',    'move');
INSERT INTO synonyms VALUES ('tiptoe', 'move');
INSERT INTO synonyms VALUES ('stomp',  'move');
INSERT INTO synonyms VALUES ('shimmy', 'move');
INSERT INTO synonyms VALUES ('crawl',  'move');