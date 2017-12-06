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
					'wait for witness',
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
	
	PRIMARY KEY (victim),
	
	FOREIGN KEY (victim) 	REFERENCES mapped_npc (mapped_id),
	FOREIGN KEY (murderer) 	REFERENCES mapped_npc (mapped_id)
);

CREATE TABLE CLUE (
	/*clue_id 	INT NOT NULL AUTO_INCREMENT,*/
	victim 		INT NOT NULL,
	witness		INT NOT NULL,
	detail 		INT NOT NULL,

	/*PRIMARY KEY (clue_id),*/
	
	FOREIGN KEY (victim) 	REFERENCES MURDER (victim),
	FOREIGN KEY (witness) 	REFERENCES MAPPED_NPC (mapped_id),
	FOREIGN KEY (detail) 	REFERENCES DETAIL (detail_id)

);
CREATE UNIQUE INDEX MOM_GAME ON CLUE (victim, witness, 	detail);

CREATE TABLE PLAYER_CLUE (
	victim 	INT NOT NULL,
	detail 	INT NOT NULL,

	PRIMARY KEY (victim, detail),

	FOREIGN KEY (victim) REFERENCES MURDER (victim),
	FOREIGN KEY (detail) REFERENCES DETAIL (detail_id)
);

INSERT INTO direction VALUES ('n', 'north');
INSERT INTO direction VALUES ('ne', 'northeast');
INSERT INTO direction VALUES ('e', 'east');
INSERT INTO direction VALUES ('se', 'southeast');
INSERT INTO direction VALUES ('s', 'south');
INSERT INTO direction VALUES ('sw', 'southwest');
INSERT INTO direction VALUES ('w', 'west');
INSERT INTO direction VALUES ('nw', 'northwest');
INSERT INTO direction VALUES ('u', 'up');
INSERT INTO direction VALUES ('d', 'down');

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

INSERT INTO detail VALUES (1, 'pocket watch', NULL);
INSERT INTO detail VALUES (2, 'red scarf', NULL);
INSERT INTO detail VALUES (3, 'duck-headed cane', NULL);
INSERT INTO detail VALUES (4, 'flower of clove', NULL);
INSERT INTO detail VALUES (5, 'hat with feathers', NULL);
INSERT INTO detail VALUES (6, 'thick moustache', NULL);
INSERT INTO detail VALUES (7, 'some sauce on their clothes', NULL);
INSERT INTO detail VALUES (8, 'pearl necklace', NULL);
INSERT INTO detail VALUES (9, 'lace collar', null);
INSERT INTO detail VALUES (10, 'flashy earrings', null);
INSERT INTO detail VALUES (11, 'pompous cravat', NULL);
INSERT INTO detail VALUES (13, 'bulging manhood', NULL);
INSERT INTO detail VALUES (12, 'extravagant monocle', NULL);
INSERT INTO detail VALUES (14, 'wine glass in pocket', null);
INSERT INTO detail VALUES (15, 'long boots', null);
INSERT INTO detail VALUES (16, 'deep blue eyes', null);
INSERT INTO detail VALUES (17, 'blood red lips', null);
INSERT INTO detail VALUES (18, 'scar on face', null);
INSERT INTO detail VALUES (19, 'dagger on their belt', null);
INSERT INTO detail VALUES (20, 'thick eyeglasses', null);

INSERT INTO detail VALUES (21, 'belt bag', null);
INSERT INTO detail VALUES (22, 'scottish kilt', null);
INSERT INTO detail VALUES (23, 'trombone', null);
INSERT INTO detail VALUES (24, 'striped pendant', null);
INSERT INTO detail VALUES (25, 'parrot on shoulder', null);
INSERT INTO detail VALUES (26, 'sad eyes', null);
INSERT INTO detail VALUES (27, 'ugly nose', null);
INSERT INTO detail VALUES (28, 'long braided hair', null);
INSERT INTO detail VALUES (29, 'highest heels ever', null);
INSERT INTO detail VALUES (30, 'mouth full of appetizers', null);
INSERT INTO detail VALUES (31, 'white handkerchief', null);
INSERT INTO detail VALUES (32, 'golden chains', null);
INSERT INTO detail VALUES (33, 'big epaulettes', null);
INSERT INTO detail VALUES (34, 'white gloves', null);
INSERT INTO detail VALUES (35, 'silver-laced vest', null);
INSERT INTO detail VALUES (36, 'tiny nosering', null);
INSERT INTO detail VALUES (37, 'loathsome tattoo', null);
INSERT INTO detail VALUES (38, 'drinking horn', null);
INSERT INTO detail VALUES (39, 'too much danduruff', null);
INSERT INTO detail VALUES (40, 'sparkling eyelashes', null);

INSERT INTO npc VALUES (1, 'snorkeldink', 'crumplehorn', 'Generic description.', 'A', 1);
INSERT INTO npc VALUES (2, 'brewery', 'chickenbroth', 'Generic description.', 'A', 1);
INSERT INTO npc VALUES (3, 'rinkydink', 'chuckecheese', 'Generic description.', 'A', 1);
INSERT INTO npc VALUES (4, 'brandenburg', 'creamsicle', 'Generic description.', 'A', 1);
INSERT INTO npc VALUES (5, 'benadryl', 'moldyspore', 'Generic description.', 'A', 2);
INSERT INTO npc VALUES (6, 'bumberstump', 'cumbercooch', 'Generic description.', 'A', 2);
INSERT INTO npc VALUES (7, 'benetton', 'camouflage', 'Generic description.', 'A', 2);
INSERT INTO npc VALUES (8, 'bentobox', 'cottagecheese', 'Generic description.', 'A', 2);
INSERT INTO npc VALUES (9, 'bombadil', 'curdlesnoot', 'Generic description.', 'A', 3);
INSERT INTO npc VALUES (10, 'buckingham', 'curdledmilk', 'Generic description.', 'A', 3);
INSERT INTO npc VALUES (11, 'boilerdang', 'vegemite', 'Generic description.', 'A', 3);
INSERT INTO npc VALUES (12, 'bandersnatch', 'countryside', 'Generic description.', 'A', 3);
INSERT INTO npc VALUES (13, 'syphilis', 'countryside', 'Generic description.', 'A', 4);
INSERT INTO npc VALUES (14, 'bunsenburner', 'cumbersnatch', 'Generic description.', 'A', 4);
INSERT INTO npc VALUES (15, 'burberry', 'crackerdong', 'Generic description.', 'A', 4);
INSERT INTO npc VALUES (16, 'baseballmitt', 'cuckooclock', 'Generic description.', 'A', 4);
INSERT INTO npc VALUES (17, 'blubberbutt', 'crimpysnitch', 'Generic description.', 'A', 5);
INSERT INTO npc VALUES (18, 'barister', 'lingerie', 'Generic description.', 'A', 5);
INSERT INTO npc VALUES (19, 'burlington', 'rivendell', 'Generic description.', 'A', 5);
INSERT INTO npc VALUES (20, 'brewery', 'curdlesnoot', 'Generic description.', 'A', 5);
INSERT INTO npc VALUES (21, 'billyray', 'nottinghill', 'Generic description.', 'B', 1);
INSERT INTO npc VALUES (22, 'bandicoot', 'crucifix', 'Generic description.', 'B', 1);
INSERT INTO npc VALUES (23, 'liverswort', 'cunningsnatch', 'Generic description.', 'B', 1);
INSERT INTO npc VALUES (24, 'snorkeldink', 'cumberbund', 'Generic description.', 'B', 1);
INSERT INTO npc VALUES (25, 'timothy', 'cummerbund', 'Generic description.', 'B', 2);
INSERT INTO npc VALUES (26, 'syphilis', 'banglesnatch', 'Generic description.', 'B', 2);
INSERT INTO npc VALUES (27, 'burberry', 'nottinghill', 'Generic description.', 'B', 2);
INSERT INTO npc VALUES (28, 'blubberdick', 'crumplehorn', 'Generic description.', 'B', 2);
INSERT INTO npc VALUES (29, 'whippersnatch', 'curdledong', 'Generic description.', 'B', 3);
INSERT INTO npc VALUES (30, 'tiddleywomp', 'cumberbund', 'Generic description.', 'B', 3);
INSERT INTO npc VALUES (31, 'bedlington', 'cheddarcheese', 'Generic description.', 'B', 3);
INSERT INTO npc VALUES (32, 'pallettown', 'chesterfield', 'Generic description.', 'B', 3);
INSERT INTO npc VALUES (33, 'brandenburg', 'carrotstick', 'Generic description.', 'B', 4);
INSERT INTO npc VALUES (34, 'boobytrap', 'crackerdong', 'Generic description.', 'B', 4);
INSERT INTO npc VALUES (35, 'tiddleywomp', 'chesterfield', 'Generic description.', 'B', 4);
INSERT INTO npc VALUES (36, 'bombadil', 'chickenbroth', 'Generic description.', 'B', 4);
INSERT INTO npc VALUES (37, 'buttermilk', 'crumplesack', 'Generic description.', 'B', 5);
INSERT INTO npc VALUES (38, 'bendandsnap', 'curdledmilk', 'Generic description.', 'B', 5);
INSERT INTO npc VALUES (39, 'benjamin', 'snickersbar', 'Generic description.', 'B', 5);
INSERT INTO npc VALUES (40, 'snozzlebert', 'snugglesnatch', 'Generic description.', 'B', 5);

INSERT INTO npc_detail VALUES (  1,   2);
INSERT INTO npc_detail VALUES (  1,   5);
INSERT INTO npc_detail VALUES (  1,   8);
INSERT INTO npc_detail VALUES (  1,  10);
INSERT INTO npc_detail VALUES (  1,  17);
INSERT INTO npc_detail VALUES (  2,   3);
INSERT INTO npc_detail VALUES (  2,   9);
INSERT INTO npc_detail VALUES (  2,  11);
INSERT INTO npc_detail VALUES (  2,  15);
INSERT INTO npc_detail VALUES (  2,  18);
INSERT INTO npc_detail VALUES (  3,   4);
INSERT INTO npc_detail VALUES (  3,   6);
INSERT INTO npc_detail VALUES (  3,   7);
INSERT INTO npc_detail VALUES (  3,  14);
INSERT INTO npc_detail VALUES (  3,  20);
INSERT INTO npc_detail VALUES (  4,   1);
INSERT INTO npc_detail VALUES (  4,  12);
INSERT INTO npc_detail VALUES (  4,  13);
INSERT INTO npc_detail VALUES (  4,  16);
INSERT INTO npc_detail VALUES (  4,  19);
INSERT INTO npc_detail VALUES (  5,   6);
INSERT INTO npc_detail VALUES (  5,  11);
INSERT INTO npc_detail VALUES (  5,  12);
INSERT INTO npc_detail VALUES (  5,  16);
INSERT INTO npc_detail VALUES (  5,  18);
INSERT INTO npc_detail VALUES (  6,   3);
INSERT INTO npc_detail VALUES (  6,   9);
INSERT INTO npc_detail VALUES (  6,  10);
INSERT INTO npc_detail VALUES (  6,  13);
INSERT INTO npc_detail VALUES (  6,  15);
INSERT INTO npc_detail VALUES (  7,   1);
INSERT INTO npc_detail VALUES (  7,   2);
INSERT INTO npc_detail VALUES (  7,   4);
INSERT INTO npc_detail VALUES (  7,  14);
INSERT INTO npc_detail VALUES (  7,  20);
INSERT INTO npc_detail VALUES (  8,   5);
INSERT INTO npc_detail VALUES (  8,   7);
INSERT INTO npc_detail VALUES (  8,   8);
INSERT INTO npc_detail VALUES (  8,  17);
INSERT INTO npc_detail VALUES (  8,  19);
INSERT INTO npc_detail VALUES (  9,   3);
INSERT INTO npc_detail VALUES (  9,   5);
INSERT INTO npc_detail VALUES (  9,  14);
INSERT INTO npc_detail VALUES (  9,  16);
INSERT INTO npc_detail VALUES (  9,  19);
INSERT INTO npc_detail VALUES ( 10,   6);
INSERT INTO npc_detail VALUES ( 10,   7);
INSERT INTO npc_detail VALUES ( 10,  11);
INSERT INTO npc_detail VALUES ( 10,  13);
INSERT INTO npc_detail VALUES ( 10,  15);
INSERT INTO npc_detail VALUES ( 11,   1);
INSERT INTO npc_detail VALUES ( 11,   2);
INSERT INTO npc_detail VALUES ( 11,  12);
INSERT INTO npc_detail VALUES ( 11,  18);
INSERT INTO npc_detail VALUES ( 11,  20);
INSERT INTO npc_detail VALUES ( 12,   4);
INSERT INTO npc_detail VALUES ( 12,   8);
INSERT INTO npc_detail VALUES ( 12,   9);
INSERT INTO npc_detail VALUES ( 12,  10);
INSERT INTO npc_detail VALUES ( 12,  17);
INSERT INTO npc_detail VALUES ( 13,   4);
INSERT INTO npc_detail VALUES ( 13,  10);
INSERT INTO npc_detail VALUES ( 13,  16);
INSERT INTO npc_detail VALUES ( 13,  17);
INSERT INTO npc_detail VALUES ( 13,  18);
INSERT INTO npc_detail VALUES ( 14,   3);
INSERT INTO npc_detail VALUES ( 14,   5);
INSERT INTO npc_detail VALUES ( 14,  13);
INSERT INTO npc_detail VALUES ( 14,  14);
INSERT INTO npc_detail VALUES ( 14,  20);
INSERT INTO npc_detail VALUES ( 15,   2);
INSERT INTO npc_detail VALUES ( 15,   6);
INSERT INTO npc_detail VALUES ( 15,   9);
INSERT INTO npc_detail VALUES ( 15,  12);
INSERT INTO npc_detail VALUES ( 15,  15);
INSERT INTO npc_detail VALUES ( 16,   1);
INSERT INTO npc_detail VALUES ( 16,   7);
INSERT INTO npc_detail VALUES ( 16,   8);
INSERT INTO npc_detail VALUES ( 16,  11);
INSERT INTO npc_detail VALUES ( 16,  19);
INSERT INTO npc_detail VALUES ( 17,   5);
INSERT INTO npc_detail VALUES ( 17,   6);
INSERT INTO npc_detail VALUES ( 17,  11);
INSERT INTO npc_detail VALUES ( 17,  13);
INSERT INTO npc_detail VALUES ( 17,  19);
INSERT INTO npc_detail VALUES ( 18,   1);
INSERT INTO npc_detail VALUES ( 18,   2);
INSERT INTO npc_detail VALUES ( 18,   4);
INSERT INTO npc_detail VALUES ( 18,  15);
INSERT INTO npc_detail VALUES ( 18,  18);
INSERT INTO npc_detail VALUES ( 19,   7);
INSERT INTO npc_detail VALUES ( 19,   8);
INSERT INTO npc_detail VALUES ( 19,  14);
INSERT INTO npc_detail VALUES ( 19,  17);
INSERT INTO npc_detail VALUES ( 19,  20);
INSERT INTO npc_detail VALUES ( 20,   3);
INSERT INTO npc_detail VALUES ( 20,   9);
INSERT INTO npc_detail VALUES ( 20,  10);
INSERT INTO npc_detail VALUES ( 20,  12);
INSERT INTO npc_detail VALUES ( 20,  16);
INSERT INTO npc_detail VALUES ( 21,  25);
INSERT INTO npc_detail VALUES ( 21,  27);
INSERT INTO npc_detail VALUES ( 21,  28);
INSERT INTO npc_detail VALUES ( 21,  31);
INSERT INTO npc_detail VALUES ( 21,  33);
INSERT INTO npc_detail VALUES ( 22,  22);
INSERT INTO npc_detail VALUES ( 22,  26);
INSERT INTO npc_detail VALUES ( 22,  29);
INSERT INTO npc_detail VALUES ( 22,  32);
INSERT INTO npc_detail VALUES ( 22,  39);
INSERT INTO npc_detail VALUES ( 23,  21);
INSERT INTO npc_detail VALUES ( 23,  24);
INSERT INTO npc_detail VALUES ( 23,  30);
INSERT INTO npc_detail VALUES ( 23,  34);
INSERT INTO npc_detail VALUES ( 23,  40);
INSERT INTO npc_detail VALUES ( 24,  23);
INSERT INTO npc_detail VALUES ( 24,  35);
INSERT INTO npc_detail VALUES ( 24,  36);
INSERT INTO npc_detail VALUES ( 24,  37);
INSERT INTO npc_detail VALUES ( 24,  38);
INSERT INTO npc_detail VALUES ( 25,  24);
INSERT INTO npc_detail VALUES ( 25,  26);
INSERT INTO npc_detail VALUES ( 25,  28);
INSERT INTO npc_detail VALUES ( 25,  34);
INSERT INTO npc_detail VALUES ( 25,  40);
INSERT INTO npc_detail VALUES ( 26,  23);
INSERT INTO npc_detail VALUES ( 26,  25);
INSERT INTO npc_detail VALUES ( 26,  27);
INSERT INTO npc_detail VALUES ( 26,  30);
INSERT INTO npc_detail VALUES ( 26,  31);
INSERT INTO npc_detail VALUES ( 27,  29);
INSERT INTO npc_detail VALUES ( 27,  33);
INSERT INTO npc_detail VALUES ( 27,  36);
INSERT INTO npc_detail VALUES ( 27,  37);
INSERT INTO npc_detail VALUES ( 27,  38);
INSERT INTO npc_detail VALUES ( 28,  21);
INSERT INTO npc_detail VALUES ( 28,  22);
INSERT INTO npc_detail VALUES ( 28,  32);
INSERT INTO npc_detail VALUES ( 28,  35);
INSERT INTO npc_detail VALUES ( 28,  39);
INSERT INTO npc_detail VALUES ( 29,  21);
INSERT INTO npc_detail VALUES ( 29,  24);
INSERT INTO npc_detail VALUES ( 29,  33);
INSERT INTO npc_detail VALUES ( 29,  36);
INSERT INTO npc_detail VALUES ( 29,  37);
INSERT INTO npc_detail VALUES ( 30,  26);
INSERT INTO npc_detail VALUES ( 30,  27);
INSERT INTO npc_detail VALUES ( 30,  30);
INSERT INTO npc_detail VALUES ( 30,  32);
INSERT INTO npc_detail VALUES ( 30,  40);
INSERT INTO npc_detail VALUES ( 31,  22);
INSERT INTO npc_detail VALUES ( 31,  25);
INSERT INTO npc_detail VALUES ( 31,  29);
INSERT INTO npc_detail VALUES ( 31,  31);
INSERT INTO npc_detail VALUES ( 31,  35);
INSERT INTO npc_detail VALUES ( 32,  23);
INSERT INTO npc_detail VALUES ( 32,  28);
INSERT INTO npc_detail VALUES ( 32,  34);
INSERT INTO npc_detail VALUES ( 32,  38);
INSERT INTO npc_detail VALUES ( 32,  39);
INSERT INTO npc_detail VALUES ( 33,  24);
INSERT INTO npc_detail VALUES ( 33,  25);
INSERT INTO npc_detail VALUES ( 33,  32);
INSERT INTO npc_detail VALUES ( 33,  36);
INSERT INTO npc_detail VALUES ( 33,  37);
INSERT INTO npc_detail VALUES ( 34,  23);
INSERT INTO npc_detail VALUES ( 34,  26);
INSERT INTO npc_detail VALUES ( 34,  33);
INSERT INTO npc_detail VALUES ( 34,  35);
INSERT INTO npc_detail VALUES ( 34,  38);
INSERT INTO npc_detail VALUES ( 35,  21);
INSERT INTO npc_detail VALUES ( 35,  29);
INSERT INTO npc_detail VALUES ( 35,  31);
INSERT INTO npc_detail VALUES ( 35,  34);
INSERT INTO npc_detail VALUES ( 35,  39);
INSERT INTO npc_detail VALUES ( 36,  22);
INSERT INTO npc_detail VALUES ( 36,  27);
INSERT INTO npc_detail VALUES ( 36,  28);
INSERT INTO npc_detail VALUES ( 36,  30);
INSERT INTO npc_detail VALUES ( 36,  40);
INSERT INTO npc_detail VALUES ( 37,  27);
INSERT INTO npc_detail VALUES ( 37,  31);
INSERT INTO npc_detail VALUES ( 37,  32);
INSERT INTO npc_detail VALUES ( 37,  35);
INSERT INTO npc_detail VALUES ( 37,  39);
INSERT INTO npc_detail VALUES ( 38,  21);
INSERT INTO npc_detail VALUES ( 38,  30);
INSERT INTO npc_detail VALUES ( 38,  36);
INSERT INTO npc_detail VALUES ( 38,  38);
INSERT INTO npc_detail VALUES ( 38,  40);
INSERT INTO npc_detail VALUES ( 39,  22);
INSERT INTO npc_detail VALUES ( 39,  23);
INSERT INTO npc_detail VALUES ( 39,  25);
INSERT INTO npc_detail VALUES ( 39,  29);
INSERT INTO npc_detail VALUES ( 39,  37);
INSERT INTO npc_detail VALUES ( 40,  24);
INSERT INTO npc_detail VALUES ( 40,  26);
INSERT INTO npc_detail VALUES ( 40,  28);
INSERT INTO npc_detail VALUES ( 40,  33);
INSERT INTO npc_detail VALUES ( 40,  34);


-- PARSER SECTION =============================================================
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

-- All other targets
CREATE TABLE specials (
	word VARCHAR(100) NOT NULL
);

CREATE TABLE synonyms (
	word VARCHAR (100) NOT NULL,
	main_word VARCHAR (100) NOT NULL
);

INSERT INTO VERB VALUES ('look');
INSERT INTO VERB VALUES ('move');
INSERT INTO VERB VALUES ('ask');
INSERT INTO VERB VALUES ('blame');
INSERT INTO VERB VALUES ('wait');

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
INSERT INTO ACTIONS VALUES (90, 'wait', False, NULL, False);

-- VERBS
INSERT INTO synonyms VALUES ('pass', 'wait');

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

-- OTHERS
INSERT INTO specials VALUES ('notes');
INSERT INTO synonyms VALUES ('memo', 'notes');