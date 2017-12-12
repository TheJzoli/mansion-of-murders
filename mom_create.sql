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

	PRIMARY KEY (detail_id)
);

CREATE TABLE NPC (
	npc_id 		INT NOT NULL,
	first_name 	VARCHAR (40) NOT NULL,
	last_name 	VARCHAR (40) NOT NULL,
	description	TEXT NOT NULL,

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
CREATE UNIQUE INDEX MOM_GAME ON CLUE (victim, witness, detail);

CREATE TABLE PLAYER_CLUE (
	victim 			INT NOT NULL,
	detail 			INT,

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

INSERT INTO room VALUES (1, 'front yard', 'A pathway lined with rose bushes leads to north to the huge, dark mansion.');
INSERT INTO two_part_words VALUES ('front', 'yard');
INSERT INTO room VALUES (2, 'entrance', 'Great doors and large pillars of marble welcome you to the entrance of the mansion. Red carpet is spread on the floor like it\'s just for you.');
INSERT INTO room VALUES (3, 'tea room', 'Dark and tall fireplace with glass doors warms up the tea room that\'s lined with soft couches and armchairs.');
INSERT INTO two_part_words VALUES ('tea', 'room');

INSERT INTO room VALUES (4, 'dining room', 'Long table already set for a one, two, ... five-course meal for at least forty people. Expensive china and crystal glasses cover the perfect white tablecloth.');
INSERT INTO two_part_words VALUES ('dining', 'room');
INSERT INTO room VALUES (5, 'bar', 'Wooden bar table and behind it what seems to be an endless supply of finest wines and whiskies in a glass cabinet. There are three red leather armchairs around the room. Please take a seat and enjoy a nice drink and a cigar.');
INSERT INTO room VALUES (6, 'kitchen', 'Ah... it smells delicious in here. Someone has been cooking a banquet in here. There\'s a large goose heating in the oven and there are several ingredients on the tables. A gorgeous cake with fresh cherries is put on the table.');

INSERT INTO room VALUES (7, 'billiard room', 'This is the billiard room named after the big billiard table in the middle that\'s sadly not been used as actively as intended. Anyway, be our guest and play a little or continue your way.');
INSERT INTO two_part_words VALUES ('billiard', 'room');
INSERT INTO room VALUES (8, 'hall', 'Boring old hallway with the same carpeting as everywhere and some dark looking paintings hanging from the walls.');
INSERT INTO room VALUES (9, 'butlers room', 'A modest bed with grey coverings and small desk with notes about household duties on it. You also notice some letters but those look private.');
INSERT INTO two_part_words VALUES ('butlers', 'room');
INSERT INTO room VALUES (10, 'music room', 'Different musical instruments lay all around the room but the most noticeable is the black grand piano right in the middle of the room. The room is weirdly shaped, but it must for the acoustics.');
INSERT INTO two_part_words VALUES ('music', 'room');
INSERT INTO room VALUES (11, 'ballroom','A beautiful ballroom perfect for dances and other formal festivities. The walls are covered in gold and a sparkly chandelier is hanging from the ceiling, the parquet floor shines like this room was never been used before. At the end of the great hall you can see large stairs that lead to upstairs. You can hear the music coming from the music room and you almost feel like boogieing.');
INSERT INTO room VALUES (12, 'terrace', 'Lovely terrace with patio furniture and some lemonade, perfect for cooling down after intense balls. When you are ready, head back to the ballroom to your north or stay and relax for a bit.');
INSERT INTO room VALUES (13, 'gallery', 'The family\'s pride: the art gallery. Hundreds of paintings hanging from the walls all framed with gold but the paintings themselves all seem to be weirdly dark. You can\'t quite figure out what they represent but they give some chills for sure.');

INSERT INTO room VALUES (14, 'servants room', 'Several grey beds in a row for all the regular servants to sleep in and small cabinet full of spare clothes for them. Messy job apparently, since the floor is covered in dirt.');
INSERT INTO two_part_words VALUES ('servants', 'room');
INSERT INTO room VALUES (15, 'maids room', 'Dirty little room for all the kitchen servants to sleep in, no wonder it smells like rotten potatoes. Nothing more to tell about this sad little room.');
INSERT INTO two_part_words VALUES ('maids', 'room');
INSERT INTO room VALUES (16, 'back yard', 'A calming scenery opens in front of your eyes as you make your way to the back yard. This is a garden-like paradise with blooming apple trees and plantings that border a little pathway.');
INSERT INTO two_part_words VALUES ('back', 'yard');
INSERT INTO room VALUES (17, 'bathroom', 'Downstairs bathroom for the servant-scums. Dirty and unhygienic bathroom with just one toilet and a bucket in a corner.' );


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
INSERT INTO passage VALUES (5, 10, 'w');
-- kitchen
INSERT INTO passage VALUES (6, 5, 's');
INSERT INTO passage VALUES (6, 11, 'sw');
INSERT INTO passage VALUES (6, 16, 'w');
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
INSERT INTO passage VALUES (10, 5, 'e');
-- ballroom
INSERT INTO passage VALUES (11, 10, 'e');
INSERT INTO passage VALUES (11, 12, 's');
INSERT INTO passage VALUES (11, 13, 'w');
INSERT INTO passage VALUES (11, 6, 'ne');
-- terrace
INSERT INTO passage VALUES (12, 11, 'n');
-- gallery
INSERT INTO passage VALUES (13, 11, 'e');
INSERT INTO passage VALUES (13, 14, 's');
-- servants
INSERT INTO passage VALUES (14, 13, 'n');
INSERT INTO passage VALUES (14, 17, 'w');
INSERT INTO passage VALUES (14, 15, 'nw');
-- kitchen maids
INSERT INTO passage VALUES (15, 17, 's');
INSERT INTO passage VALUES (15, 16, 'n');
INSERT INTO passage VALUES (15, 14, 'se');
-- back yard
INSERT INTO passage VALUES (16, 15, 's');
INSERT INTO passage VALUES (16, 6, 'e');
-- bathroom
INSERT INTO passage VALUES (17, 14, 'e');


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

INSERT INTO detail VALUES (1, 'a pocket watch');
INSERT INTO detail VALUES (2, 'a red scarf');
INSERT INTO detail VALUES (3, 'a duck-headed cane');
INSERT INTO detail VALUES (4, 'a flower of clove');
INSERT INTO detail VALUES (5, 'a hat with feathers');
INSERT INTO detail VALUES (6, 'a thick moustache');
INSERT INTO detail VALUES (7, 'some sauce on their clothes');
INSERT INTO detail VALUES (8, 'a pearl necklace');
INSERT INTO detail VALUES (9, 'a lace collar');
INSERT INTO detail VALUES (10, 'flashy earrings');
INSERT INTO detail VALUES (11, 'a pompous cravat');
INSERT INTO detail VALUES (13, 'a bulging manhood');
INSERT INTO detail VALUES (12, 'an extravagant monocle');
INSERT INTO detail VALUES (14, 'a wine glass in pocket');
INSERT INTO detail VALUES (15, 'long boots');
INSERT INTO detail VALUES (16, 'deep blue eyes');
INSERT INTO detail VALUES (17, 'blood red lips');
INSERT INTO detail VALUES (18, 'a scar on their face');
INSERT INTO detail VALUES (19, 'a dagger on their belt');
INSERT INTO detail VALUES (20, 'thick eyeglasses');

INSERT INTO detail VALUES (21, 'a belt bag');
INSERT INTO detail VALUES (22, 'a Scottish kilt');
INSERT INTO detail VALUES (23, 'a trombone');
INSERT INTO detail VALUES (24, 'a striped pendant');
INSERT INTO detail VALUES (25, 'a parrot on their shoulder');
INSERT INTO detail VALUES (26, 'sad eyes');
INSERT INTO detail VALUES (27, 'an ugly nose');
INSERT INTO detail VALUES (28, 'long braided hair');
INSERT INTO detail VALUES (29, 'the highest heels ever');
INSERT INTO detail VALUES (30, 'a mouth full of appetizers');
INSERT INTO detail VALUES (31, 'a white handkerchief');
INSERT INTO detail VALUES (32, 'golden chains');
INSERT INTO detail VALUES (33, 'big epaulettes');
INSERT INTO detail VALUES (34, 'white gloves');
INSERT INTO detail VALUES (35, 'a silver-laced vest');
INSERT INTO detail VALUES (36, 'a tiny nosering');
INSERT INTO detail VALUES (37, 'a loathsome tattoo');
INSERT INTO detail VALUES (38, 'drinking horn');
INSERT INTO detail VALUES (39, 'too much danduruff');
INSERT INTO detail VALUES (40, 'sparkling eyelashes');
INSERT INTO detail VALUES (41, 'thight knickerbockers');
INSERT INTO detail VALUES (42, 'massive bruise');
INSERT INTO detail VALUES (43, 'pointy shoes');
INSERT INTO detail VALUES (44, 'they are missing a finger');
INSERT INTO detail VALUES (45, 'red ears');
INSERT INTO detail VALUES (46, 'divine voice');
INSERT INTO detail VALUES (47, 'they are sweating like a pig');
INSERT INTO detail VALUES (48, 'bushy eyebrows');
INSERT INTO detail VALUES (49, 'wrinkled bow-tie');
INSERT INTO detail VALUES (50, 'milk on their moustache');

INSERT INTO npc VALUES (1, 'snorkeldink', 'crumplehorn', 'You definitely notice this man even from afar. If his great stomach or even greater laugh doesn\'t do the trick, the bushy moustache will. Of course, being the host and all, his always dressed to his best; dark tail coat and a top hat.', 'A', 1);
INSERT INTO npc VALUES (2, 'brewery', 'chickenbroth', 'This handsome young fellow looks like he could swoon the tournures off from all the ladies. He\'s looks so stylish and modern with his sideburns and a new blazer that\'s the latest fashion. What a show of.', 'A', 1);
INSERT INTO npc VALUES (3, 'rinkydink', 'chuckecheese', 'Oh, this poor awkward looking little bastard. He looks so skinny; the wind could blow him away any second. His tuxedo looks somehow too small and too big at the same time and the fact that he\'s a ginger like his whole family doesn\'t help him at all.', 'A', 1);
INSERT INTO npc VALUES (4, 'brandenburg', 'creamsicle', 'This must be the only man who has made ginger work. He looks tall and handsome and his tuxedo is a perfect fit unlike his brother\'s.', 'A', 1);
INSERT INTO npc VALUES (5,'burgerking','thundercatch','The lord\'s unfortunate little brother. He was born with ginger hair and curly nose hairs. He looks a little short and chubby in his tail coat, but at least he seems to be happy.','A',1);
INSERT INTO npc VALUES (6, 'benadryl', 'moldyspore', 'He\'s a boring-looking man. Grey hair, grey suit, greyish skin, everything about this poor man screams for the permission to retire.', 'A', 2);
INSERT INTO npc VALUES (7, 'bumberstump', 'cumbercooch', 'He looks very old. He\'s being serving the family for generations and he\'s as loyal as they come but he\'s an old-fashioned man. He wears the same gloves and vest he has worn since the 1830\'s and swears under his breath whenever someone tries something new.', 'A', 2);
INSERT INTO npc VALUES (8, 'benetton', 'camouflage', 'The lord\'s right hand and his daily source of dirty jokes. This middle-aged man looks straight and honest and he likes to keep his looks simple and practical.', 'A', 2);
INSERT INTO npc VALUES (9, 'bentobox', 'cottagecheese', 'The stable master\'s younger son. He\'s still a child but you notice right away that he\'s a little simple-minded. He has tried to wear something fancy for this party, but he\'s only white shirt is upside-down.', 'A', 2);
INSERT INTO npc VALUES (10,'butawhiteboy','cantbekhan','Old and wise man this one. He\'s well-mannered and calm which is why he is so good with the horses. You can see the age affecting to his face already, but it doesn\'t affect his smile at all. He looks worried about his two sons though.','A',2);
INSERT INTO npc VALUES (11, 'bombadil', 'curdlesnoot', 'The stable master\'s older son. This young man looks strong and healthy, sculpted by his physical labour at the stables. If he weren\'t a servant you\'d say he\'s quite handsome as well.', 'A', 3);
INSERT INTO npc VALUES (12, 'buckingham', 'curdledmilk', 'This one looks a little mean. Maybe it\'s his huge grey eyebrows, maybe the way he walks in a hunch tapping his fingers together, who knows. But you must admit that for a man his age he is in quite a good shape.', 'A', 3);
INSERT INTO npc VALUES (13, 'boilerdang', 'vegemite', 'He looks young and eager. He is taller than anyone in the house, but he manages to keep out of the way. Still he seems to be a little distracted all the time.', 'A', 3);
INSERT INTO npc VALUES (14, 'bandersnatch', 'countryside', 'Like a scout this one is always ready. He is a small boy, but perfect for his tea-serving job. His gloves and bowtie are the same shade of cream, but his teeth have gone yellow from all the tea and coffee he\'s sneaked. That\'s probably also the reason why he\'s shaking.', 'A', 3);
INSERT INTO npc VALUES (15,'nozzlebert','ampersand','Poor man has forgot to take off his gardener\'s gloves. He\'s still put on a cravat and his Sunday pants for the occasion, so he\'s trying. It\'s the first time he\'s been allowed inside the mansion.','A',3);
INSERT INTO npc VALUES (16, 'syphilis', 'countryside', 'He looks like he\'s been made for hunting. He is big and strong, and his tweed jacket is tailored for the sport. He\'s still wearing his muddy boots and his Newsboy cap, and you wonder if he always smells like gunpowder.', 'A', 4);
INSERT INTO npc VALUES (17, 'bunsenburner', 'cumbersnatch', 'Looks like he\'s tired of this place and all the people. That\'s what all day of opening doors and driving people around does to a man. And the family is clearly not paying him enough, looking at the hand-me-down tuxedo he\'s wearing.', 'A', 4);
INSERT INTO npc VALUES (18, 'burberry', 'crackerdong', 'He looks like a very proud man. His sideburns have merged with his light beard and his eyes are deep blue, but still he looks a bit intimidating in his dark dinner jacket.', 'A', 4);
INSERT INTO npc VALUES (19, 'baseballmitt', 'cuckooclock', 'He looks like he doesn\'t want to be here. The soon-to-be-18-year-old looks handsome but uncomfortable in his brand-new tuxedo.', 'A', 4);
INSERT INTO npc VALUES (20,'biblical','concubine','A spirited little man taking after his big brother. He looks more than happy about wearing his brother\'s old suit and shoes.','A',4);
INSERT INTO npc VALUES (21, 'blubberbutt', 'crimpysnitch', 'An old man wearing even older frock coat and a top hat. His sideburns have turned white and fragile over the years, but he still has the energy to shout misogynistic obscenities at every given chance.', 'A', 5);
INSERT INTO npc VALUES (22, 'barister', 'lingerie', 'You see the largest man you\'ve ever laid your eyes upon. Dear god what has he eaten?  He has stains all over his tuxedo and his hair looks greasy.', 'A', 5);
INSERT INTO npc VALUES (23, 'burlington', 'rivendell', 'Being nobleman shows all over this man\'s face. He\'s wearing multiple rings and a monocle. How fancy.', 'A', 5);
INSERT INTO npc VALUES (24, 'brewery', 'curdlesnoot', 'This man\'s moustache is glorious. It goes down the sides of his mouth and connects to his sideburns making it look bigger. Must be a rich man if he can afford to take care of a facial hair like that.', 'A', 5);
INSERT INTO npc VALUES (25,'anglerfish','concubine','A bit ladylike appearance. He\'s hair is blonde and curly, and he seems to be admiring himself from the mirror in his hand.','A',5);
INSERT INTO npc VALUES (26, 'billyray', 'nottinghill', 'A young man, maybe German. He looks very tired and a little sad, but his outfit is the nicest you\'ve seen yet.', 'B', 1);
INSERT INTO npc VALUES (27, 'bandicoot', 'crucifix', 'Maybe a 13-year-old young lad with hair as dark as coal and a coy smile. He looks shy in his knickerbockers and leather shoes but maybe he\'s just bored. Poor boy.', 'B', 1);
INSERT INTO npc VALUES (28, 'liverswort', 'cunningsnatch', 'Skinny fellow. He has a long coat that covers some of the thinness, but you see it from his face. His hair looks great though, and he smells like fresh sea wind.', 'B', 1);
INSERT INTO npc VALUES (29, 'snorkeldink', 'cumberbund', 'He looks very arrogant. He looks down on everybody and walks like he owns the place. Maybe it\'s his high status or his flashy jewels and tuxedo, but this man seems very unlikable.', 'B', 1);
INSERT INTO npc VALUES (30,'bakery','snugglesnatch','He looks like a dandy in his dark tail coat he has decorated with golden embroidery. His hair is combed back, and his teeth are pearly white.','B',1);
INSERT INTO npc VALUES (31, 'timothy', 'cummerbund', 'Sneaky looking French gentleman. He has little curly moustache he rubs between his fingers. He is thin but the suit he is wearing covers it perfectly.', 'B', 2);
INSERT INTO npc VALUES (32, 'syphilis', 'banglesnatch', 'This man looks exotic. He has tan and clothes from distant countries. He looks like a diplomat and you don\'t recognise his accent.', 'B', 2);
INSERT INTO npc VALUES (33, 'burberry', 'nottinghill', 'Look at this man\'s ears, they\'re huge! But you don\'t make fun of this man since he is almost the most influential man in England.', 'B', 2);
INSERT INTO npc VALUES (34, 'blubberdick', 'crumplehorn', 'Poorly dressed young boy. He\'s probably one of the kitchen servants who\'s sneaked into the party.', 'B', 2);
INSERT INTO npc VALUES (35,'bendandsnap','clavichord','He is maybe middle-aged. His hair is a little grey and his starting to get bald, but he looks active and healthy. His shoes look expensive.','B',2);
INSERT INTO npc VALUES (36, 'whippersnatch', 'curdledong', 'This man is visibly drunk. His nose is red, and he struggles to stand without swaying. He reeks like cheap whisky and his jacket looks wet.', 'B', 3);
INSERT INTO npc VALUES (37, 'tiddleywomp', 'cumberbund', 'Uh, this man is ugly. His suit is sharp, his hair is gorgeous and he\'s hilarious, but you just don\'t want to look at his face.', 'B', 3);
INSERT INTO npc VALUES (38, 'bedlington', 'cheddarcheese', 'Prettiest man you\'ve ever seen. His face is peachy and his eyes sparkle. The breeches his wearing make his bottom look fabulous.', 'B', 3);
INSERT INTO npc VALUES (39, 'pallettown', 'chesterfield', 'Powerful young boy. He inherited their family\'s lands when his father died so he\'s the richest child in here. Unfortunately, he didn\'t inherit his father\'s sense of style.', 'B', 3);
INSERT INTO npc VALUES (40,'blasphemy','cumbercooch','What a lovely old man in a sack coat. He is completely bald and some of his teeth are missing but he looks delightful.','B',3);
INSERT INTO npc VALUES (41, 'brandenburg', 'carrotstick', 'This man is dressed like a commoner. But you\'ve seen his pictures hanging on the walls. Maybe it\'s a disguise but most likely he just wants to get a little break from all the fuss.', 'B', 4);
INSERT INTO npc VALUES (42, 'boobytrap', 'crackerdong', 'Life has treated this man poorly. Scars cover his face and his other ear is cut in half. He\'s dressed in dark clothing that covers the signs of child abuse.', 'B', 4);
INSERT INTO npc VALUES (43, 'tiddleywomp', 'chesterfield', 'He looks like he\'s been very lucky in life. He has a full silver hair and a wide smile. He looks handsome in his navy-blue sack coat and you\'ve heard his wife was once the most beautiful girl in England.', 'B', 4);
INSERT INTO npc VALUES (44, 'bombadil', 'chickenbroth', 'He looks a little jumpy. He\'s pale and his hair is thin and seems to be shedding all over the floors. The grey four-button suit he\'s wearing looks new.', 'B', 4);
INSERT INTO npc VALUES (45,'benjamin', 'chowderpants','Peculiar man this one. He\'s bug-eyed and short, but he looks heavy. His suit doesn\'t quite fit his figure.','B',4);
INSERT INTO npc VALUES (46, 'buttermilk', 'crumplesack', 'Looks like he\'s going to be sick. His skin is something between white and green and he keeps swaying from one side to another.', 'B', 5);
INSERT INTO npc VALUES (47, 'bendandsnap', 'curdledmilk', 'His coat is ragged, and trousers look second-hand. It\'s weird that he was invited in the first place, since he is so obviously poor.', 'B', 5);
INSERT INTO npc VALUES (48, 'benjamin', 'snickersbar', 'Funny-looking little man. He\'s wearing over-sized green suit and a dotted bow-tie. Otherwise he\'s normal-sized but his feet are abnormally large.', 'B', 5);
INSERT INTO npc VALUES (49, 'snozzlebert', 'snugglesnatch', 'He\'s a sad man crying in the corners and slowly sipping from his not-so-secret flask.  His hair is a mess and so appears to be his life.', 'B', 5);
INSERT INTO npc VALUES (50,'buttercup', 'covergirl','You look at the man and the only thing that comes to your mind is Ebenezer Scrooge from the Christmas Carol. His back is hunched, his hair and sideburns are white and he\'s wearing a long black frock coat and a dusty top hat. What a miser.','B',5);

INSERT INTO npc_detail VALUES (  1,   1);
INSERT INTO npc_detail VALUES (  1,  11);
INSERT INTO npc_detail VALUES (  1,  12);
INSERT INTO npc_detail VALUES (  1,  21);
INSERT INTO npc_detail VALUES (  1,  22);
INSERT INTO npc_detail VALUES (  2,   2);
INSERT INTO npc_detail VALUES (  2,   4);
INSERT INTO npc_detail VALUES (  2,  10);
INSERT INTO npc_detail VALUES (  2,  19);
INSERT INTO npc_detail VALUES (  2,  24);
INSERT INTO npc_detail VALUES (  3,   7);
INSERT INTO npc_detail VALUES (  3,  17);
INSERT INTO npc_detail VALUES (  3,  18);
INSERT INTO npc_detail VALUES (  3,  20);
INSERT INTO npc_detail VALUES (  3,  23);
INSERT INTO npc_detail VALUES (  4,   3);
INSERT INTO npc_detail VALUES (  4,   5);
INSERT INTO npc_detail VALUES (  4,   6);
INSERT INTO npc_detail VALUES (  4,  14);
INSERT INTO npc_detail VALUES (  4,  25);
INSERT INTO npc_detail VALUES (  5,   8);
INSERT INTO npc_detail VALUES (  5,   9);
INSERT INTO npc_detail VALUES (  5,  13);
INSERT INTO npc_detail VALUES (  5,  15);
INSERT INTO npc_detail VALUES (  5,  16);
INSERT INTO npc_detail VALUES (  6,   1);
INSERT INTO npc_detail VALUES (  6,   6);
INSERT INTO npc_detail VALUES (  6,   8);
INSERT INTO npc_detail VALUES (  6,  19);
INSERT INTO npc_detail VALUES (  6,  23);
INSERT INTO npc_detail VALUES (  7,   7);
INSERT INTO npc_detail VALUES (  7,  11);
INSERT INTO npc_detail VALUES (  7,  16);
INSERT INTO npc_detail VALUES (  7,  20);
INSERT INTO npc_detail VALUES (  7,  21);
INSERT INTO npc_detail VALUES (  8,   9);
INSERT INTO npc_detail VALUES (  8,  12);
INSERT INTO npc_detail VALUES (  8,  15);
INSERT INTO npc_detail VALUES (  8,  17);
INSERT INTO npc_detail VALUES (  8,  18);
INSERT INTO npc_detail VALUES (  9,   2);
INSERT INTO npc_detail VALUES (  9,   5);
INSERT INTO npc_detail VALUES (  9,  14);
INSERT INTO npc_detail VALUES (  9,  24);
INSERT INTO npc_detail VALUES (  9,  25);
INSERT INTO npc_detail VALUES ( 10,   3);
INSERT INTO npc_detail VALUES ( 10,   4);
INSERT INTO npc_detail VALUES ( 10,  10);
INSERT INTO npc_detail VALUES ( 10,  13);
INSERT INTO npc_detail VALUES ( 10,  22);
INSERT INTO npc_detail VALUES ( 11,   4);
INSERT INTO npc_detail VALUES ( 11,   8);
INSERT INTO npc_detail VALUES ( 11,  11);
INSERT INTO npc_detail VALUES ( 11,  14);
INSERT INTO npc_detail VALUES ( 11,  19);
INSERT INTO npc_detail VALUES ( 12,   6);
INSERT INTO npc_detail VALUES ( 12,  10);
INSERT INTO npc_detail VALUES ( 12,  12);
INSERT INTO npc_detail VALUES ( 12,  13);
INSERT INTO npc_detail VALUES ( 12,  18);
INSERT INTO npc_detail VALUES ( 13,   2);
INSERT INTO npc_detail VALUES ( 13,  16);
INSERT INTO npc_detail VALUES ( 13,  17);
INSERT INTO npc_detail VALUES ( 13,  20);
INSERT INTO npc_detail VALUES ( 13,  24);
INSERT INTO npc_detail VALUES ( 14,   7);
INSERT INTO npc_detail VALUES ( 14,   9);
INSERT INTO npc_detail VALUES ( 14,  15);
INSERT INTO npc_detail VALUES ( 14,  21);
INSERT INTO npc_detail VALUES ( 14,  25);
INSERT INTO npc_detail VALUES ( 15,   1);
INSERT INTO npc_detail VALUES ( 15,   3);
INSERT INTO npc_detail VALUES ( 15,   5);
INSERT INTO npc_detail VALUES ( 15,  22);
INSERT INTO npc_detail VALUES ( 15,  23);
INSERT INTO npc_detail VALUES ( 16,   1);
INSERT INTO npc_detail VALUES ( 16,   4);
INSERT INTO npc_detail VALUES ( 16,   6);
INSERT INTO npc_detail VALUES ( 16,   8);
INSERT INTO npc_detail VALUES ( 16,  14);
INSERT INTO npc_detail VALUES ( 17,   7);
INSERT INTO npc_detail VALUES ( 17,  16);
INSERT INTO npc_detail VALUES ( 17,  17);
INSERT INTO npc_detail VALUES ( 17,  20);
INSERT INTO npc_detail VALUES ( 17,  21);
INSERT INTO npc_detail VALUES ( 18,   2);
INSERT INTO npc_detail VALUES ( 18,  12);
INSERT INTO npc_detail VALUES ( 18,  18);
INSERT INTO npc_detail VALUES ( 18,  19);
INSERT INTO npc_detail VALUES ( 18,  25);
INSERT INTO npc_detail VALUES ( 19,   3);
INSERT INTO npc_detail VALUES ( 19,  10);
INSERT INTO npc_detail VALUES ( 19,  13);
INSERT INTO npc_detail VALUES ( 19,  15);
INSERT INTO npc_detail VALUES ( 19,  23);
INSERT INTO npc_detail VALUES ( 20,   5);
INSERT INTO npc_detail VALUES ( 20,   9);
INSERT INTO npc_detail VALUES ( 20,  11);
INSERT INTO npc_detail VALUES ( 20,  22);
INSERT INTO npc_detail VALUES ( 20,  24);
INSERT INTO npc_detail VALUES ( 21,   1);
INSERT INTO npc_detail VALUES ( 21,  13);
INSERT INTO npc_detail VALUES ( 21,  15);
INSERT INTO npc_detail VALUES ( 21,  19);
INSERT INTO npc_detail VALUES ( 21,  25);
INSERT INTO npc_detail VALUES ( 22,   3);
INSERT INTO npc_detail VALUES ( 22,   6);
INSERT INTO npc_detail VALUES ( 22,   9);
INSERT INTO npc_detail VALUES ( 22,  14);
INSERT INTO npc_detail VALUES ( 22,  23);
INSERT INTO npc_detail VALUES ( 23,   7);
INSERT INTO npc_detail VALUES ( 23,   8);
INSERT INTO npc_detail VALUES ( 23,  17);
INSERT INTO npc_detail VALUES ( 23,  18);
INSERT INTO npc_detail VALUES ( 23,  21);
INSERT INTO npc_detail VALUES ( 24,  10);
INSERT INTO npc_detail VALUES ( 24,  16);
INSERT INTO npc_detail VALUES ( 24,  20);
INSERT INTO npc_detail VALUES ( 24,  22);
INSERT INTO npc_detail VALUES ( 24,  24);
INSERT INTO npc_detail VALUES ( 25,   2);
INSERT INTO npc_detail VALUES ( 25,   4);
INSERT INTO npc_detail VALUES ( 25,   5);
INSERT INTO npc_detail VALUES ( 25,  11);
INSERT INTO npc_detail VALUES ( 25,  12);
INSERT INTO npc_detail VALUES ( 26,  32);
INSERT INTO npc_detail VALUES ( 26,  37);
INSERT INTO npc_detail VALUES ( 26,  38);
INSERT INTO npc_detail VALUES ( 26,  42);
INSERT INTO npc_detail VALUES ( 26,  46);
INSERT INTO npc_detail VALUES ( 27,  26);
INSERT INTO npc_detail VALUES ( 27,  27);
INSERT INTO npc_detail VALUES ( 27,  31);
INSERT INTO npc_detail VALUES ( 27,  35);
INSERT INTO npc_detail VALUES ( 27,  48);
INSERT INTO npc_detail VALUES ( 28,  34);
INSERT INTO npc_detail VALUES ( 28,  39);
INSERT INTO npc_detail VALUES ( 28,  43);
INSERT INTO npc_detail VALUES ( 28,  44);
INSERT INTO npc_detail VALUES ( 28,  47);
INSERT INTO npc_detail VALUES ( 29,  29);
INSERT INTO npc_detail VALUES ( 29,  33);
INSERT INTO npc_detail VALUES ( 29,  40);
INSERT INTO npc_detail VALUES ( 29,  41);
INSERT INTO npc_detail VALUES ( 29,  45);
INSERT INTO npc_detail VALUES ( 30,  28);
INSERT INTO npc_detail VALUES ( 30,  30);
INSERT INTO npc_detail VALUES ( 30,  36);
INSERT INTO npc_detail VALUES ( 30,  49);
INSERT INTO npc_detail VALUES ( 30,  50);
INSERT INTO npc_detail VALUES ( 31,  34);
INSERT INTO npc_detail VALUES ( 31,  37);
INSERT INTO npc_detail VALUES ( 31,  42);
INSERT INTO npc_detail VALUES ( 31,  43);
INSERT INTO npc_detail VALUES ( 31,  47);
INSERT INTO npc_detail VALUES ( 32,  27);
INSERT INTO npc_detail VALUES ( 32,  29);
INSERT INTO npc_detail VALUES ( 32,  33);
INSERT INTO npc_detail VALUES ( 32,  35);
INSERT INTO npc_detail VALUES ( 32,  49);
INSERT INTO npc_detail VALUES ( 33,  38);
INSERT INTO npc_detail VALUES ( 33,  39);
INSERT INTO npc_detail VALUES ( 33,  41);
INSERT INTO npc_detail VALUES ( 33,  46);
INSERT INTO npc_detail VALUES ( 33,  50);
INSERT INTO npc_detail VALUES ( 34,  30);
INSERT INTO npc_detail VALUES ( 34,  31);
INSERT INTO npc_detail VALUES ( 34,  32);
INSERT INTO npc_detail VALUES ( 34,  44);
INSERT INTO npc_detail VALUES ( 34,  45);
INSERT INTO npc_detail VALUES ( 35,  26);
INSERT INTO npc_detail VALUES ( 35,  28);
INSERT INTO npc_detail VALUES ( 35,  36);
INSERT INTO npc_detail VALUES ( 35,  40);
INSERT INTO npc_detail VALUES ( 35,  48);
INSERT INTO npc_detail VALUES ( 36,  40);
INSERT INTO npc_detail VALUES ( 36,  41);
INSERT INTO npc_detail VALUES ( 36,  43);
INSERT INTO npc_detail VALUES ( 36,  44);
INSERT INTO npc_detail VALUES ( 36,  48);
INSERT INTO npc_detail VALUES ( 37,  26);
INSERT INTO npc_detail VALUES ( 37,  29);
INSERT INTO npc_detail VALUES ( 37,  30);
INSERT INTO npc_detail VALUES ( 37,  35);
INSERT INTO npc_detail VALUES ( 37,  49);
INSERT INTO npc_detail VALUES ( 38,  31);
INSERT INTO npc_detail VALUES ( 38,  37);
INSERT INTO npc_detail VALUES ( 38,  39);
INSERT INTO npc_detail VALUES ( 38,  42);
INSERT INTO npc_detail VALUES ( 38,  50);
INSERT INTO npc_detail VALUES ( 39,  27);
INSERT INTO npc_detail VALUES ( 39,  32);
INSERT INTO npc_detail VALUES ( 39,  34);
INSERT INTO npc_detail VALUES ( 39,  45);
INSERT INTO npc_detail VALUES ( 39,  47);
INSERT INTO npc_detail VALUES ( 40,  28);
INSERT INTO npc_detail VALUES ( 40,  33);
INSERT INTO npc_detail VALUES ( 40,  36);
INSERT INTO npc_detail VALUES ( 40,  38);
INSERT INTO npc_detail VALUES ( 40,  46);
INSERT INTO npc_detail VALUES ( 41,  31);
INSERT INTO npc_detail VALUES ( 41,  33);
INSERT INTO npc_detail VALUES ( 41,  34);
INSERT INTO npc_detail VALUES ( 41,  35);
INSERT INTO npc_detail VALUES ( 41,  37);
INSERT INTO npc_detail VALUES ( 42,  27);
INSERT INTO npc_detail VALUES ( 42,  32);
INSERT INTO npc_detail VALUES ( 42,  36);
INSERT INTO npc_detail VALUES ( 42,  39);
INSERT INTO npc_detail VALUES ( 42,  46);
INSERT INTO npc_detail VALUES ( 43,  26);
INSERT INTO npc_detail VALUES ( 43,  40);
INSERT INTO npc_detail VALUES ( 43,  44);
INSERT INTO npc_detail VALUES ( 43,  45);
INSERT INTO npc_detail VALUES ( 43,  48);
INSERT INTO npc_detail VALUES ( 44,  41);
INSERT INTO npc_detail VALUES ( 44,  42);
INSERT INTO npc_detail VALUES ( 44,  43);
INSERT INTO npc_detail VALUES ( 44,  49);
INSERT INTO npc_detail VALUES ( 44,  50);
INSERT INTO npc_detail VALUES ( 45,  28);
INSERT INTO npc_detail VALUES ( 45,  29);
INSERT INTO npc_detail VALUES ( 45,  30);
INSERT INTO npc_detail VALUES ( 45,  38);
INSERT INTO npc_detail VALUES ( 45,  47);
INSERT INTO npc_detail VALUES ( 46,  29);
INSERT INTO npc_detail VALUES ( 46,  33);
INSERT INTO npc_detail VALUES ( 46,  36);
INSERT INTO npc_detail VALUES ( 46,  40);
INSERT INTO npc_detail VALUES ( 46,  47);
INSERT INTO npc_detail VALUES ( 47,  26);
INSERT INTO npc_detail VALUES ( 47,  28);
INSERT INTO npc_detail VALUES ( 47,  31);
INSERT INTO npc_detail VALUES ( 47,  37);
INSERT INTO npc_detail VALUES ( 47,  42);
INSERT INTO npc_detail VALUES ( 48,  32);
INSERT INTO npc_detail VALUES ( 48,  35);
INSERT INTO npc_detail VALUES ( 48,  39);
INSERT INTO npc_detail VALUES ( 48,  45);
INSERT INTO npc_detail VALUES ( 48,  48);
INSERT INTO npc_detail VALUES ( 49,  41);
INSERT INTO npc_detail VALUES ( 49,  43);
INSERT INTO npc_detail VALUES ( 49,  46);
INSERT INTO npc_detail VALUES ( 49,  49);
INSERT INTO npc_detail VALUES ( 49,  50);
INSERT INTO npc_detail VALUES ( 50,  27);
INSERT INTO npc_detail VALUES ( 50,  30);
INSERT INTO npc_detail VALUES ( 50,  34);
INSERT INTO npc_detail VALUES ( 50,  38);
INSERT INTO npc_detail VALUES ( 50,  44);


-- PARSER SECTION =============================================================
CREATE TABLE VERB (
	word VARCHAR(100),
	PRIMARY KEY (word)
);

CREATE TABLE ALL_VERBS (
	word VARCHAR (100)
);

CREATE TABLE CURSES (
	word VARCHAR(100)
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

INSERT INTO actions VALUES (10, 'move', False, 'to', True);
INSERT INTO actions VALUES (11, 'move', False, NULL, True);
INSERT INTO actions VALUES (20, 'look', False, 'at', True);
INSERT INTO actions VALUES (21, 'look', False, 'around', False);
INSERT INTO actions VALUES (21, 'look', False, NULL, FALSE);
INSERT INTO actions VALUES (30, 'ask', True, 'about', True);
INSERT INTO actions VALUES (31, 'ask', False, 'about', True);
INSERT INTO actions VALUES (31, 'ask', True, null, False);
INSERT INTO actions VALUES (40, 'blame', True, 'for killing', True);
INSERT INTO actions VALUES (90, 'wait', False, NULL, False);

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
INSERT INTO specials VALUES ('ragequit');
INSERT INTO synonyms VALUES ('rage quit', 'ragequit');
INSERT INTO two_part_words VALUES ('rage', 'quit');

INSERT INTO curses VALUES ('arse');
INSERT INTO curses VALUES ('ass');
INSERT INTO curses VALUES ('asshole');
INSERT INTO curses VALUES ('bastard');
INSERT INTO curses VALUES ('bitch');
INSERT INTO curses VALUES ('bollocks');
INSERT INTO curses VALUES ('crap');
INSERT INTO curses VALUES ('cunt');
INSERT INTO curses VALUES ('damn');
INSERT INTO curses VALUES ('fuck');
INSERT INTO curses VALUES ('fucker');
INSERT INTO curses VALUES ('fucking');
INSERT INTO curses VALUES ('fucks');
INSERT INTO curses VALUES ('goddamn');
INSERT INTO curses VALUES ('goddamnit');
INSERT INTO curses VALUES ('motherfucker');
INSERT INTO curses VALUES ('hell');
INSERT INTO curses VALUES ('nigga');
INSERT INTO curses VALUES ('nigger');
INSERT INTO curses VALUES ('shit');
INSERT INTO curses VALUES ('shitting');
INSERT INTO curses VALUES ('shitass');
INSERT INTO curses VALUES ('twat');
INSERT INTO curses VALUES ('cum');
INSERT INTO curses VALUES ('cumming');
INSERT INTO curses VALUES ('penis');
INSERT INTO curses VALUES ('dick');
INSERT INTO curses VALUES ('faggot');
INSERT INTO curses VALUES ('vagina');
INSERT INTO curses VALUES ('pussy');
INSERT INTO curses VALUES ('benis');


-- ALL VERBS
INSERT INTO all_verbs VALUES ('abash');
INSERT INTO all_verbs VALUES ('abate');
INSERT INTO all_verbs VALUES ('abide');
INSERT INTO all_verbs VALUES ('absorb');
INSERT INTO all_verbs VALUES ('accept');
INSERT INTO all_verbs VALUES ('accompany');
INSERT INTO all_verbs VALUES ('ache');
INSERT INTO all_verbs VALUES ('achieve');
INSERT INTO all_verbs VALUES ('acquire');
INSERT INTO all_verbs VALUES ('act');
INSERT INTO all_verbs VALUES ('add');
INSERT INTO all_verbs VALUES ('address');
INSERT INTO all_verbs VALUES ('adjust');
INSERT INTO all_verbs VALUES ('admire');
INSERT INTO all_verbs VALUES ('admit');
INSERT INTO all_verbs VALUES ('advise');
INSERT INTO all_verbs VALUES ('afford');
INSERT INTO all_verbs VALUES ('agree');
INSERT INTO all_verbs VALUES ('alight');
INSERT INTO all_verbs VALUES ('allow');
INSERT INTO all_verbs VALUES ('animate');
INSERT INTO all_verbs VALUES ('announce');
INSERT INTO all_verbs VALUES ('answer');
INSERT INTO all_verbs VALUES ('apologize');
INSERT INTO all_verbs VALUES ('appear');
INSERT INTO all_verbs VALUES ('applaud');
INSERT INTO all_verbs VALUES ('apply');
INSERT INTO all_verbs VALUES ('approach');
INSERT INTO all_verbs VALUES ('approve');
INSERT INTO all_verbs VALUES ('argue');
INSERT INTO all_verbs VALUES ('arise');
INSERT INTO all_verbs VALUES ('arrange');
INSERT INTO all_verbs VALUES ('arrest');
INSERT INTO all_verbs VALUES ('ask');
INSERT INTO all_verbs VALUES ('assert');
INSERT INTO all_verbs VALUES ('assort');
INSERT INTO all_verbs VALUES ('astonish');
INSERT INTO all_verbs VALUES ('attack');
INSERT INTO all_verbs VALUES ('attend');
INSERT INTO all_verbs VALUES ('attract');
INSERT INTO all_verbs VALUES ('audit');
INSERT INTO all_verbs VALUES ('avoid');
INSERT INTO all_verbs VALUES ('awake');
INSERT INTO all_verbs VALUES ('bang');
INSERT INTO all_verbs VALUES ('banish');
INSERT INTO all_verbs VALUES ('bash');
INSERT INTO all_verbs VALUES ('bat');
INSERT INTO all_verbs VALUES ('be');
INSERT INTO all_verbs VALUES ('bear');
INSERT INTO all_verbs VALUES ('bear');
INSERT INTO all_verbs VALUES ('beat');
INSERT INTO all_verbs VALUES ('beautify');
INSERT INTO all_verbs VALUES ('become');
INSERT INTO all_verbs VALUES ('befall');
INSERT INTO all_verbs VALUES ('beg');
INSERT INTO all_verbs VALUES ('begin');
INSERT INTO all_verbs VALUES ('behave');
INSERT INTO all_verbs VALUES ('behold');
INSERT INTO all_verbs VALUES ('believe');
INSERT INTO all_verbs VALUES ('belong');
INSERT INTO all_verbs VALUES ('bend');
INSERT INTO all_verbs VALUES ('bereave');
INSERT INTO all_verbs VALUES ('beseech');
INSERT INTO all_verbs VALUES ('bet');
INSERT INTO all_verbs VALUES ('betray');
INSERT INTO all_verbs VALUES ('bid');
INSERT INTO all_verbs VALUES ('bid');
INSERT INTO all_verbs VALUES ('bind');
INSERT INTO all_verbs VALUES ('bite');
INSERT INTO all_verbs VALUES ('blame');
INSERT INTO all_verbs VALUES ('bleed');
INSERT INTO all_verbs VALUES ('bless');
INSERT INTO all_verbs VALUES ('blossom');
INSERT INTO all_verbs VALUES ('blow');
INSERT INTO all_verbs VALUES ('blur');
INSERT INTO all_verbs VALUES ('blush');
INSERT INTO all_verbs VALUES ('board');
INSERT INTO all_verbs VALUES ('boast');
INSERT INTO all_verbs VALUES ('boil');
INSERT INTO all_verbs VALUES ('bow');
INSERT INTO all_verbs VALUES ('box');
INSERT INTO all_verbs VALUES ('bray');
INSERT INTO all_verbs VALUES ('break');
INSERT INTO all_verbs VALUES ('breathe');
INSERT INTO all_verbs VALUES ('breed');
INSERT INTO all_verbs VALUES ('bring');
INSERT INTO all_verbs VALUES ('broadcast');
INSERT INTO all_verbs VALUES ('brush');
INSERT INTO all_verbs VALUES ('build');
INSERT INTO all_verbs VALUES ('burn');
INSERT INTO all_verbs VALUES ('burst');
INSERT INTO all_verbs VALUES ('bury');
INSERT INTO all_verbs VALUES ('bust');
INSERT INTO all_verbs VALUES ('buy');
INSERT INTO all_verbs VALUES ('buzz');
INSERT INTO all_verbs VALUES ('calculate');
INSERT INTO all_verbs VALUES ('call');
INSERT INTO all_verbs VALUES ('canvass');
INSERT INTO all_verbs VALUES ('capture');
INSERT INTO all_verbs VALUES ('caress');
INSERT INTO all_verbs VALUES ('carry');
INSERT INTO all_verbs VALUES ('carve');
INSERT INTO all_verbs VALUES ('cash');
INSERT INTO all_verbs VALUES ('cast');
INSERT INTO all_verbs VALUES ('catch');
INSERT INTO all_verbs VALUES ('cause');
INSERT INTO all_verbs VALUES ('cease');
INSERT INTO all_verbs VALUES ('celebrate');
INSERT INTO all_verbs VALUES ('challenge');
INSERT INTO all_verbs VALUES ('change');
INSERT INTO all_verbs VALUES ('charge');
INSERT INTO all_verbs VALUES ('chase');
INSERT INTO all_verbs VALUES ('chat');
INSERT INTO all_verbs VALUES ('check');
INSERT INTO all_verbs VALUES ('cheer');
INSERT INTO all_verbs VALUES ('chew');
INSERT INTO all_verbs VALUES ('chide');
INSERT INTO all_verbs VALUES ('chip');
INSERT INTO all_verbs VALUES ('choke');
INSERT INTO all_verbs VALUES ('choose');
INSERT INTO all_verbs VALUES ('classify');
INSERT INTO all_verbs VALUES ('clean');
INSERT INTO all_verbs VALUES ('cleave');
INSERT INTO all_verbs VALUES ('click');
INSERT INTO all_verbs VALUES ('climb');
INSERT INTO all_verbs VALUES ('cling');
INSERT INTO all_verbs VALUES ('close');
INSERT INTO all_verbs VALUES ('clothe');
INSERT INTO all_verbs VALUES ('clutch');
INSERT INTO all_verbs VALUES ('collapse');
INSERT INTO all_verbs VALUES ('collect');
INSERT INTO all_verbs VALUES ('colour');
INSERT INTO all_verbs VALUES ('come');
INSERT INTO all_verbs VALUES ('comment');
INSERT INTO all_verbs VALUES ('compare');
INSERT INTO all_verbs VALUES ('compel');
INSERT INTO all_verbs VALUES ('compete');
INSERT INTO all_verbs VALUES ('complain');
INSERT INTO all_verbs VALUES ('complete');
INSERT INTO all_verbs VALUES ('conclude');
INSERT INTO all_verbs VALUES ('conduct');
INSERT INTO all_verbs VALUES ('confess');
INSERT INTO all_verbs VALUES ('confine');
INSERT INTO all_verbs VALUES ('confiscate');
INSERT INTO all_verbs VALUES ('confuse');
INSERT INTO all_verbs VALUES ('congratulate');
INSERT INTO all_verbs VALUES ('connect');
INSERT INTO all_verbs VALUES ('connote');
INSERT INTO all_verbs VALUES ('conquer');
INSERT INTO all_verbs VALUES ('consecrate');
INSERT INTO all_verbs VALUES ('consent');
INSERT INTO all_verbs VALUES ('conserve');
INSERT INTO all_verbs VALUES ('consider');
INSERT INTO all_verbs VALUES ('consign');
INSERT INTO all_verbs VALUES ('consist');
INSERT INTO all_verbs VALUES ('console');
INSERT INTO all_verbs VALUES ('consort');
INSERT INTO all_verbs VALUES ('conspire');
INSERT INTO all_verbs VALUES ('constitute');
INSERT INTO all_verbs VALUES ('constrain');
INSERT INTO all_verbs VALUES ('construct');
INSERT INTO all_verbs VALUES ('construe');
INSERT INTO all_verbs VALUES ('consult');
INSERT INTO all_verbs VALUES ('contain');
INSERT INTO all_verbs VALUES ('contemn');
INSERT INTO all_verbs VALUES ('contend');
INSERT INTO all_verbs VALUES ('contest');
INSERT INTO all_verbs VALUES ('continue');
INSERT INTO all_verbs VALUES ('contract');
INSERT INTO all_verbs VALUES ('contradict');
INSERT INTO all_verbs VALUES ('contrast');
INSERT INTO all_verbs VALUES ('contribute');
INSERT INTO all_verbs VALUES ('contrive');
INSERT INTO all_verbs VALUES ('control');
INSERT INTO all_verbs VALUES ('convene');
INSERT INTO all_verbs VALUES ('converge');
INSERT INTO all_verbs VALUES ('converse');
INSERT INTO all_verbs VALUES ('convert');
INSERT INTO all_verbs VALUES ('convey');
INSERT INTO all_verbs VALUES ('convict');
INSERT INTO all_verbs VALUES ('convince');
INSERT INTO all_verbs VALUES ('coo');
INSERT INTO all_verbs VALUES ('cook');
INSERT INTO all_verbs VALUES ('cool');
INSERT INTO all_verbs VALUES ('co-operate');
INSERT INTO all_verbs VALUES ('cope');
INSERT INTO all_verbs VALUES ('copy');
INSERT INTO all_verbs VALUES ('correct');
INSERT INTO all_verbs VALUES ('correspond');
INSERT INTO all_verbs VALUES ('corrode');
INSERT INTO all_verbs VALUES ('corrupt');
INSERT INTO all_verbs VALUES ('cost');
INSERT INTO all_verbs VALUES ('cough');
INSERT INTO all_verbs VALUES ('counsel');
INSERT INTO all_verbs VALUES ('count');
INSERT INTO all_verbs VALUES ('course');
INSERT INTO all_verbs VALUES ('cover');
INSERT INTO all_verbs VALUES ('cower');
INSERT INTO all_verbs VALUES ('crack');
INSERT INTO all_verbs VALUES ('crackle');
INSERT INTO all_verbs VALUES ('crash');
INSERT INTO all_verbs VALUES ('crave');
INSERT INTO all_verbs VALUES ('create');
INSERT INTO all_verbs VALUES ('creep');
INSERT INTO all_verbs VALUES ('crib');
INSERT INTO all_verbs VALUES ('cross');
INSERT INTO all_verbs VALUES ('crowd');
INSERT INTO all_verbs VALUES ('crush');
INSERT INTO all_verbs VALUES ('cry');
INSERT INTO all_verbs VALUES ('curb');
INSERT INTO all_verbs VALUES ('cure');
INSERT INTO all_verbs VALUES ('curve');
INSERT INTO all_verbs VALUES ('cut');
INSERT INTO all_verbs VALUES ('cycle');
INSERT INTO all_verbs VALUES ('damage');
INSERT INTO all_verbs VALUES ('damp');
INSERT INTO all_verbs VALUES ('dance');
INSERT INTO all_verbs VALUES ('dare');
INSERT INTO all_verbs VALUES ('dash');
INSERT INTO all_verbs VALUES ('dazzle');
INSERT INTO all_verbs VALUES ('deal');
INSERT INTO all_verbs VALUES ('decay');
INSERT INTO all_verbs VALUES ('decide');
INSERT INTO all_verbs VALUES ('declare');
INSERT INTO all_verbs VALUES ('decorate');
INSERT INTO all_verbs VALUES ('decrease');
INSERT INTO all_verbs VALUES ('dedicate');
INSERT INTO all_verbs VALUES ('delay');
INSERT INTO all_verbs VALUES ('delete');
INSERT INTO all_verbs VALUES ('deny');
INSERT INTO all_verbs VALUES ('depend');
INSERT INTO all_verbs VALUES ('deprive');
INSERT INTO all_verbs VALUES ('derive');
INSERT INTO all_verbs VALUES ('describe');
INSERT INTO all_verbs VALUES ('desire');
INSERT INTO all_verbs VALUES ('destroy');
INSERT INTO all_verbs VALUES ('detach');
INSERT INTO all_verbs VALUES ('detect');
INSERT INTO all_verbs VALUES ('determine');
INSERT INTO all_verbs VALUES ('develop');
INSERT INTO all_verbs VALUES ('die');
INSERT INTO all_verbs VALUES ('differ');
INSERT INTO all_verbs VALUES ('dig');
INSERT INTO all_verbs VALUES ('digest');
INSERT INTO all_verbs VALUES ('dim');
INSERT INTO all_verbs VALUES ('diminish');
INSERT INTO all_verbs VALUES ('dine');
INSERT INTO all_verbs VALUES ('dip');
INSERT INTO all_verbs VALUES ('direct');
INSERT INTO all_verbs VALUES ('disappear');
INSERT INTO all_verbs VALUES ('discover');
INSERT INTO all_verbs VALUES ('discuss');
INSERT INTO all_verbs VALUES ('disobey');
INSERT INTO all_verbs VALUES ('display');
INSERT INTO all_verbs VALUES ('dispose');
INSERT INTO all_verbs VALUES ('distribute');
INSERT INTO all_verbs VALUES ('disturb');
INSERT INTO all_verbs VALUES ('disuse');
INSERT INTO all_verbs VALUES ('dive');
INSERT INTO all_verbs VALUES ('divide');
INSERT INTO all_verbs VALUES ('do');
INSERT INTO all_verbs VALUES ('donate');
INSERT INTO all_verbs VALUES ('download');
INSERT INTO all_verbs VALUES ('drag');
INSERT INTO all_verbs VALUES ('draw');
INSERT INTO all_verbs VALUES ('dream');
INSERT INTO all_verbs VALUES ('dress');
INSERT INTO all_verbs VALUES ('drill');
INSERT INTO all_verbs VALUES ('drink');
INSERT INTO all_verbs VALUES ('drive');
INSERT INTO all_verbs VALUES ('drop');
INSERT INTO all_verbs VALUES ('dry');
INSERT INTO all_verbs VALUES ('dump');
INSERT INTO all_verbs VALUES ('dwell');
INSERT INTO all_verbs VALUES ('dye');
INSERT INTO all_verbs VALUES ('earn');
INSERT INTO all_verbs VALUES ('eat');
INSERT INTO all_verbs VALUES ('educate');
INSERT INTO all_verbs VALUES ('empower');
INSERT INTO all_verbs VALUES ('empty');
INSERT INTO all_verbs VALUES ('encircle');
INSERT INTO all_verbs VALUES ('encourage');
INSERT INTO all_verbs VALUES ('encroach');
INSERT INTO all_verbs VALUES ('endanger');
INSERT INTO all_verbs VALUES ('endorse');
INSERT INTO all_verbs VALUES ('endure');
INSERT INTO all_verbs VALUES ('engrave');
INSERT INTO all_verbs VALUES ('enjoy');
INSERT INTO all_verbs VALUES ('enlarge');
INSERT INTO all_verbs VALUES ('enlighten');
INSERT INTO all_verbs VALUES ('enter');
INSERT INTO all_verbs VALUES ('envy');
INSERT INTO all_verbs VALUES ('erase');
INSERT INTO all_verbs VALUES ('escape');
INSERT INTO all_verbs VALUES ('evaporate');
INSERT INTO all_verbs VALUES ('exchange');
INSERT INTO all_verbs VALUES ('exclaim');
INSERT INTO all_verbs VALUES ('exclude');
INSERT INTO all_verbs VALUES ('exist');
INSERT INTO all_verbs VALUES ('expand');
INSERT INTO all_verbs VALUES ('expect');
INSERT INTO all_verbs VALUES ('explain');
INSERT INTO all_verbs VALUES ('explore');
INSERT INTO all_verbs VALUES ('express');
INSERT INTO all_verbs VALUES ('extend');
INSERT INTO all_verbs VALUES ('eye');
INSERT INTO all_verbs VALUES ('face');
INSERT INTO all_verbs VALUES ('fail');
INSERT INTO all_verbs VALUES ('faint');
INSERT INTO all_verbs VALUES ('fall');
INSERT INTO all_verbs VALUES ('fan');
INSERT INTO all_verbs VALUES ('fancy');
INSERT INTO all_verbs VALUES ('favour');
INSERT INTO all_verbs VALUES ('fax');
INSERT INTO all_verbs VALUES ('feed');
INSERT INTO all_verbs VALUES ('feel');
INSERT INTO all_verbs VALUES ('ferry');
INSERT INTO all_verbs VALUES ('fetch');
INSERT INTO all_verbs VALUES ('fight');
INSERT INTO all_verbs VALUES ('fill');
INSERT INTO all_verbs VALUES ('find');
INSERT INTO all_verbs VALUES ('finish');
INSERT INTO all_verbs VALUES ('fish');
INSERT INTO all_verbs VALUES ('fit');
INSERT INTO all_verbs VALUES ('fix');
INSERT INTO all_verbs VALUES ('fizz');
INSERT INTO all_verbs VALUES ('flap');
INSERT INTO all_verbs VALUES ('flash');
INSERT INTO all_verbs VALUES ('flee');
INSERT INTO all_verbs VALUES ('fling');
INSERT INTO all_verbs VALUES ('float');
INSERT INTO all_verbs VALUES ('flop');
INSERT INTO all_verbs VALUES ('fly');
INSERT INTO all_verbs VALUES ('fold');
INSERT INTO all_verbs VALUES ('follow');
INSERT INTO all_verbs VALUES ('forbid');
INSERT INTO all_verbs VALUES ('force');
INSERT INTO all_verbs VALUES ('forecast');
INSERT INTO all_verbs VALUES ('foretell');
INSERT INTO all_verbs VALUES ('forget');
INSERT INTO all_verbs VALUES ('forgive');
INSERT INTO all_verbs VALUES ('forlese');
INSERT INTO all_verbs VALUES ('form');
INSERT INTO all_verbs VALUES ('forsake');
INSERT INTO all_verbs VALUES ('found');
INSERT INTO all_verbs VALUES ('frame');
INSERT INTO all_verbs VALUES ('free');
INSERT INTO all_verbs VALUES ('freeze');
INSERT INTO all_verbs VALUES ('frighten');
INSERT INTO all_verbs VALUES ('fry');
INSERT INTO all_verbs VALUES ('fulfil');
INSERT INTO all_verbs VALUES ('gag');
INSERT INTO all_verbs VALUES ('gain');
INSERT INTO all_verbs VALUES ('gainsay');
INSERT INTO all_verbs VALUES ('gash');
INSERT INTO all_verbs VALUES ('gaze');
INSERT INTO all_verbs VALUES ('get');
INSERT INTO all_verbs VALUES ('give');
INSERT INTO all_verbs VALUES ('glance');
INSERT INTO all_verbs VALUES ('glitter');
INSERT INTO all_verbs VALUES ('glow');
INSERT INTO all_verbs VALUES ('go');
INSERT INTO all_verbs VALUES ('google');
INSERT INTO all_verbs VALUES ('govern');
INSERT INTO all_verbs VALUES ('grab');
INSERT INTO all_verbs VALUES ('grade');
INSERT INTO all_verbs VALUES ('grant');
INSERT INTO all_verbs VALUES ('greet');
INSERT INTO all_verbs VALUES ('grind');
INSERT INTO all_verbs VALUES ('grip');
INSERT INTO all_verbs VALUES ('grow');
INSERT INTO all_verbs VALUES ('guard');
INSERT INTO all_verbs VALUES ('guess');
INSERT INTO all_verbs VALUES ('guide');
INSERT INTO all_verbs VALUES ('hack');
INSERT INTO all_verbs VALUES ('handle');
INSERT INTO all_verbs VALUES ('hang');
INSERT INTO all_verbs VALUES ('happen');
INSERT INTO all_verbs VALUES ('harm');
INSERT INTO all_verbs VALUES ('hatch');
INSERT INTO all_verbs VALUES ('hate');
INSERT INTO all_verbs VALUES ('have');
INSERT INTO all_verbs VALUES ('heal');
INSERT INTO all_verbs VALUES ('hear');
INSERT INTO all_verbs VALUES ('heave');
INSERT INTO all_verbs VALUES ('help');
INSERT INTO all_verbs VALUES ('hew');
INSERT INTO all_verbs VALUES ('hide');
INSERT INTO all_verbs VALUES ('hinder');
INSERT INTO all_verbs VALUES ('hiss');
INSERT INTO all_verbs VALUES ('hit');
INSERT INTO all_verbs VALUES ('hoax');
INSERT INTO all_verbs VALUES ('hold');
INSERT INTO all_verbs VALUES ('hop');
INSERT INTO all_verbs VALUES ('hope');
INSERT INTO all_verbs VALUES ('horrify');
INSERT INTO all_verbs VALUES ('hug');
INSERT INTO all_verbs VALUES ('hum');
INSERT INTO all_verbs VALUES ('humiliate');
INSERT INTO all_verbs VALUES ('hunch');
INSERT INTO all_verbs VALUES ('hunt');
INSERT INTO all_verbs VALUES ('hurl');
INSERT INTO all_verbs VALUES ('hurry');
INSERT INTO all_verbs VALUES ('hurt');
INSERT INTO all_verbs VALUES ('hush');
INSERT INTO all_verbs VALUES ('hustle');
INSERT INTO all_verbs VALUES ('hypnotize');
INSERT INTO all_verbs VALUES ('idealize');
INSERT INTO all_verbs VALUES ('identify');
INSERT INTO all_verbs VALUES ('idolize');
INSERT INTO all_verbs VALUES ('ignite');
INSERT INTO all_verbs VALUES ('ignore');
INSERT INTO all_verbs VALUES ('ill-treat');
INSERT INTO all_verbs VALUES ('illuminate');
INSERT INTO all_verbs VALUES ('illumine');
INSERT INTO all_verbs VALUES ('illustrate');
INSERT INTO all_verbs VALUES ('imagine');
INSERT INTO all_verbs VALUES ('imbibe');
INSERT INTO all_verbs VALUES ('imitate');
INSERT INTO all_verbs VALUES ('immerse');
INSERT INTO all_verbs VALUES ('immolate');
INSERT INTO all_verbs VALUES ('immure');
INSERT INTO all_verbs VALUES ('impair');
INSERT INTO all_verbs VALUES ('impart');
INSERT INTO all_verbs VALUES ('impeach');
INSERT INTO all_verbs VALUES ('impede');
INSERT INTO all_verbs VALUES ('impel');
INSERT INTO all_verbs VALUES ('impend');
INSERT INTO all_verbs VALUES ('imperil');
INSERT INTO all_verbs VALUES ('impinge');
INSERT INTO all_verbs VALUES ('implant');
INSERT INTO all_verbs VALUES ('implicate');
INSERT INTO all_verbs VALUES ('implode');
INSERT INTO all_verbs VALUES ('implore');
INSERT INTO all_verbs VALUES ('imply');
INSERT INTO all_verbs VALUES ('import');
INSERT INTO all_verbs VALUES ('impose');
INSERT INTO all_verbs VALUES ('impress');
INSERT INTO all_verbs VALUES ('imprint');
INSERT INTO all_verbs VALUES ('imprison');
INSERT INTO all_verbs VALUES ('improve');
INSERT INTO all_verbs VALUES ('inaugurate');
INSERT INTO all_verbs VALUES ('incise');
INSERT INTO all_verbs VALUES ('include');
INSERT INTO all_verbs VALUES ('increase');
INSERT INTO all_verbs VALUES ('inculcate');
INSERT INTO all_verbs VALUES ('indent');
INSERT INTO all_verbs VALUES ('indicate');
INSERT INTO all_verbs VALUES ('induce');
INSERT INTO all_verbs VALUES ('indulge');
INSERT INTO all_verbs VALUES ('infect');
INSERT INTO all_verbs VALUES ('infest');
INSERT INTO all_verbs VALUES ('inflame');
INSERT INTO all_verbs VALUES ('inflate');
INSERT INTO all_verbs VALUES ('inflect');
INSERT INTO all_verbs VALUES ('inform');
INSERT INTO all_verbs VALUES ('infringe');
INSERT INTO all_verbs VALUES ('infuse');
INSERT INTO all_verbs VALUES ('ingest');
INSERT INTO all_verbs VALUES ('inhabit');
INSERT INTO all_verbs VALUES ('inhale');
INSERT INTO all_verbs VALUES ('inherit');
INSERT INTO all_verbs VALUES ('initiate');
INSERT INTO all_verbs VALUES ('inject');
INSERT INTO all_verbs VALUES ('injure');
INSERT INTO all_verbs VALUES ('inlay');
INSERT INTO all_verbs VALUES ('innovate');
INSERT INTO all_verbs VALUES ('input');
INSERT INTO all_verbs VALUES ('inquire');
INSERT INTO all_verbs VALUES ('inscribe');
INSERT INTO all_verbs VALUES ('insert');
INSERT INTO all_verbs VALUES ('inspect');
INSERT INTO all_verbs VALUES ('inspire');
INSERT INTO all_verbs VALUES ('install');
INSERT INTO all_verbs VALUES ('insult');
INSERT INTO all_verbs VALUES ('insure');
INSERT INTO all_verbs VALUES ('integrate');
INSERT INTO all_verbs VALUES ('introduce');
INSERT INTO all_verbs VALUES ('invent');
INSERT INTO all_verbs VALUES ('invite');
INSERT INTO all_verbs VALUES ('join');
INSERT INTO all_verbs VALUES ('jump');
INSERT INTO all_verbs VALUES ('justify');
INSERT INTO all_verbs VALUES ('keep');
INSERT INTO all_verbs VALUES ('kick');
INSERT INTO all_verbs VALUES ('kid');
INSERT INTO all_verbs VALUES ('kill');
INSERT INTO all_verbs VALUES ('kiss');
INSERT INTO all_verbs VALUES ('kneel');
INSERT INTO all_verbs VALUES ('knit');
INSERT INTO all_verbs VALUES ('knock');
INSERT INTO all_verbs VALUES ('know');
INSERT INTO all_verbs VALUES ('lade');
INSERT INTO all_verbs VALUES ('land');
INSERT INTO all_verbs VALUES ('last');
INSERT INTO all_verbs VALUES ('latch');
INSERT INTO all_verbs VALUES ('laugh');
INSERT INTO all_verbs VALUES ('lay');
INSERT INTO all_verbs VALUES ('lead');
INSERT INTO all_verbs VALUES ('leak');
INSERT INTO all_verbs VALUES ('lean');
INSERT INTO all_verbs VALUES ('leap');
INSERT INTO all_verbs VALUES ('learn');
INSERT INTO all_verbs VALUES ('leave');
INSERT INTO all_verbs VALUES ('leer');
INSERT INTO all_verbs VALUES ('lend');
INSERT INTO all_verbs VALUES ('let');
INSERT INTO all_verbs VALUES ('lick');
INSERT INTO all_verbs VALUES ('lie');
INSERT INTO all_verbs VALUES ('lie');
INSERT INTO all_verbs VALUES ('lift');
INSERT INTO all_verbs VALUES ('light');
INSERT INTO all_verbs VALUES ('like');
INSERT INTO all_verbs VALUES ('limp');
INSERT INTO all_verbs VALUES ('listen');
INSERT INTO all_verbs VALUES ('live');
INSERT INTO all_verbs VALUES ('look');
INSERT INTO all_verbs VALUES ('lose');
INSERT INTO all_verbs VALUES ('love');
INSERT INTO all_verbs VALUES ('magnify');
INSERT INTO all_verbs VALUES ('maintain');
INSERT INTO all_verbs VALUES ('make');
INSERT INTO all_verbs VALUES ('manage');
INSERT INTO all_verbs VALUES ('march');
INSERT INTO all_verbs VALUES ('mark');
INSERT INTO all_verbs VALUES ('marry');
INSERT INTO all_verbs VALUES ('mash');
INSERT INTO all_verbs VALUES ('match');
INSERT INTO all_verbs VALUES ('matter');
INSERT INTO all_verbs VALUES ('mean');
INSERT INTO all_verbs VALUES ('measure');
INSERT INTO all_verbs VALUES ('meet');
INSERT INTO all_verbs VALUES ('melt');
INSERT INTO all_verbs VALUES ('merge');
INSERT INTO all_verbs VALUES ('mew');
INSERT INTO all_verbs VALUES ('migrate');
INSERT INTO all_verbs VALUES ('milk');
INSERT INTO all_verbs VALUES ('mind');
INSERT INTO all_verbs VALUES ('mislead');
INSERT INTO all_verbs VALUES ('miss');
INSERT INTO all_verbs VALUES ('mistake');
INSERT INTO all_verbs VALUES ('misuse');
INSERT INTO all_verbs VALUES ('mix');
INSERT INTO all_verbs VALUES ('moan');
INSERT INTO all_verbs VALUES ('modify');
INSERT INTO all_verbs VALUES ('moo');
INSERT INTO all_verbs VALUES ('motivate');
INSERT INTO all_verbs VALUES ('mould');
INSERT INTO all_verbs VALUES ('moult');
INSERT INTO all_verbs VALUES ('move');
INSERT INTO all_verbs VALUES ('mow');
INSERT INTO all_verbs VALUES ('multiply');
INSERT INTO all_verbs VALUES ('murmur');
INSERT INTO all_verbs VALUES ('nail');
INSERT INTO all_verbs VALUES ('nap');
INSERT INTO all_verbs VALUES ('need');
INSERT INTO all_verbs VALUES ('neglect');
INSERT INTO all_verbs VALUES ('nip');
INSERT INTO all_verbs VALUES ('nod');
INSERT INTO all_verbs VALUES ('note');
INSERT INTO all_verbs VALUES ('notice');
INSERT INTO all_verbs VALUES ('notify');
INSERT INTO all_verbs VALUES ('nourish');
INSERT INTO all_verbs VALUES ('nurse');
INSERT INTO all_verbs VALUES ('obey');
INSERT INTO all_verbs VALUES ('oblige');
INSERT INTO all_verbs VALUES ('observe');
INSERT INTO all_verbs VALUES ('obstruct');
INSERT INTO all_verbs VALUES ('obtain');
INSERT INTO all_verbs VALUES ('occupy');
INSERT INTO all_verbs VALUES ('occur');
INSERT INTO all_verbs VALUES ('offer');
INSERT INTO all_verbs VALUES ('offset');
INSERT INTO all_verbs VALUES ('omit');
INSERT INTO all_verbs VALUES ('ooze');
INSERT INTO all_verbs VALUES ('open');
INSERT INTO all_verbs VALUES ('operate');
INSERT INTO all_verbs VALUES ('opine');
INSERT INTO all_verbs VALUES ('oppress');
INSERT INTO all_verbs VALUES ('opt');
INSERT INTO all_verbs VALUES ('optimize');
INSERT INTO all_verbs VALUES ('order');
INSERT INTO all_verbs VALUES ('organize');
INSERT INTO all_verbs VALUES ('originate');
INSERT INTO all_verbs VALUES ('output');
INSERT INTO all_verbs VALUES ('overflow');
INSERT INTO all_verbs VALUES ('overtake');
INSERT INTO all_verbs VALUES ('owe');
INSERT INTO all_verbs VALUES ('own');
INSERT INTO all_verbs VALUES ('pacify');
INSERT INTO all_verbs VALUES ('paint');
INSERT INTO all_verbs VALUES ('pardon');
INSERT INTO all_verbs VALUES ('part');
INSERT INTO all_verbs VALUES ('partake');
INSERT INTO all_verbs VALUES ('participate');
INSERT INTO all_verbs VALUES ('pass');
INSERT INTO all_verbs VALUES ('paste');
INSERT INTO all_verbs VALUES ('pat');
INSERT INTO all_verbs VALUES ('patch');
INSERT INTO all_verbs VALUES ('pause');
INSERT INTO all_verbs VALUES ('pay');
INSERT INTO all_verbs VALUES ('peep');
INSERT INTO all_verbs VALUES ('perish');
INSERT INTO all_verbs VALUES ('permit');
INSERT INTO all_verbs VALUES ('persuade');
INSERT INTO all_verbs VALUES ('phone');
INSERT INTO all_verbs VALUES ('pick');
INSERT INTO all_verbs VALUES ('place');
INSERT INTO all_verbs VALUES ('plan');
INSERT INTO all_verbs VALUES ('play');
INSERT INTO all_verbs VALUES ('plead');
INSERT INTO all_verbs VALUES ('please');
INSERT INTO all_verbs VALUES ('plod');
INSERT INTO all_verbs VALUES ('plot');
INSERT INTO all_verbs VALUES ('pluck');
INSERT INTO all_verbs VALUES ('ply');
INSERT INTO all_verbs VALUES ('point');
INSERT INTO all_verbs VALUES ('polish');
INSERT INTO all_verbs VALUES ('pollute');
INSERT INTO all_verbs VALUES ('ponder');
INSERT INTO all_verbs VALUES ('pour');
INSERT INTO all_verbs VALUES ('pout');
INSERT INTO all_verbs VALUES ('practise');
INSERT INTO all_verbs VALUES ('praise');
INSERT INTO all_verbs VALUES ('pray');
INSERT INTO all_verbs VALUES ('preach');
INSERT INTO all_verbs VALUES ('prefer');
INSERT INTO all_verbs VALUES ('prepare');
INSERT INTO all_verbs VALUES ('prescribe');
INSERT INTO all_verbs VALUES ('present');
INSERT INTO all_verbs VALUES ('preserve');
INSERT INTO all_verbs VALUES ('preset');
INSERT INTO all_verbs VALUES ('preside');
INSERT INTO all_verbs VALUES ('press');
INSERT INTO all_verbs VALUES ('pretend');
INSERT INTO all_verbs VALUES ('prevent');
INSERT INTO all_verbs VALUES ('print');
INSERT INTO all_verbs VALUES ('proceed');
INSERT INTO all_verbs VALUES ('produce');
INSERT INTO all_verbs VALUES ('progress');
INSERT INTO all_verbs VALUES ('prohibit');
INSERT INTO all_verbs VALUES ('promise');
INSERT INTO all_verbs VALUES ('propose');
INSERT INTO all_verbs VALUES ('prosecute');
INSERT INTO all_verbs VALUES ('protect');
INSERT INTO all_verbs VALUES ('prove');
INSERT INTO all_verbs VALUES ('provide');
INSERT INTO all_verbs VALUES ('pull');
INSERT INTO all_verbs VALUES ('punish');
INSERT INTO all_verbs VALUES ('purify');
INSERT INTO all_verbs VALUES ('push');
INSERT INTO all_verbs VALUES ('put');
INSERT INTO all_verbs VALUES ('qualify');
INSERT INTO all_verbs VALUES ('quarrel');
INSERT INTO all_verbs VALUES ('question');
INSERT INTO all_verbs VALUES ('quit');
INSERT INTO all_verbs VALUES ('race');
INSERT INTO all_verbs VALUES ('rain');
INSERT INTO all_verbs VALUES ('rattle');
INSERT INTO all_verbs VALUES ('reach');
INSERT INTO all_verbs VALUES ('read');
INSERT INTO all_verbs VALUES ('realize');
INSERT INTO all_verbs VALUES ('rebuild');
INSERT INTO all_verbs VALUES ('recall');
INSERT INTO all_verbs VALUES ('recast');
INSERT INTO all_verbs VALUES ('receive');
INSERT INTO all_verbs VALUES ('recite');
INSERT INTO all_verbs VALUES ('recognize');
INSERT INTO all_verbs VALUES ('recollect');
INSERT INTO all_verbs VALUES ('recur');
INSERT INTO all_verbs VALUES ('redo');
INSERT INTO all_verbs VALUES ('reduce');
INSERT INTO all_verbs VALUES ('refer');
INSERT INTO all_verbs VALUES ('reflect');
INSERT INTO all_verbs VALUES ('refuse');
INSERT INTO all_verbs VALUES ('regard');
INSERT INTO all_verbs VALUES ('regret');
INSERT INTO all_verbs VALUES ('relate');
INSERT INTO all_verbs VALUES ('relax');
INSERT INTO all_verbs VALUES ('rely');
INSERT INTO all_verbs VALUES ('remain');
INSERT INTO all_verbs VALUES ('remake');
INSERT INTO all_verbs VALUES ('remove');
INSERT INTO all_verbs VALUES ('rend');
INSERT INTO all_verbs VALUES ('renew');
INSERT INTO all_verbs VALUES ('renounce');
INSERT INTO all_verbs VALUES ('repair');
INSERT INTO all_verbs VALUES ('repeat');
INSERT INTO all_verbs VALUES ('replace');
INSERT INTO all_verbs VALUES ('reply');
INSERT INTO all_verbs VALUES ('report');
INSERT INTO all_verbs VALUES ('request');
INSERT INTO all_verbs VALUES ('resell');
INSERT INTO all_verbs VALUES ('resemble');
INSERT INTO all_verbs VALUES ('reset');
INSERT INTO all_verbs VALUES ('resist');
INSERT INTO all_verbs VALUES ('resolve');
INSERT INTO all_verbs VALUES ('respect');
INSERT INTO all_verbs VALUES ('rest');
INSERT INTO all_verbs VALUES ('restrain');
INSERT INTO all_verbs VALUES ('retain');
INSERT INTO all_verbs VALUES ('retch');
INSERT INTO all_verbs VALUES ('retire');
INSERT INTO all_verbs VALUES ('return');
INSERT INTO all_verbs VALUES ('reuse');
INSERT INTO all_verbs VALUES ('review');
INSERT INTO all_verbs VALUES ('rewind');
INSERT INTO all_verbs VALUES ('rid');
INSERT INTO all_verbs VALUES ('ride');
INSERT INTO all_verbs VALUES ('ring');
INSERT INTO all_verbs VALUES ('rise');
INSERT INTO all_verbs VALUES ('roar');
INSERT INTO all_verbs VALUES ('rob');
INSERT INTO all_verbs VALUES ('roll');
INSERT INTO all_verbs VALUES ('rot');
INSERT INTO all_verbs VALUES ('rub');
INSERT INTO all_verbs VALUES ('rule');
INSERT INTO all_verbs VALUES ('run');
INSERT INTO all_verbs VALUES ('rush');
INSERT INTO all_verbs VALUES ('sabotage');
INSERT INTO all_verbs VALUES ('sack');
INSERT INTO all_verbs VALUES ('sacrifice');
INSERT INTO all_verbs VALUES ('sadden');
INSERT INTO all_verbs VALUES ('saddle');
INSERT INTO all_verbs VALUES ('sag');
INSERT INTO all_verbs VALUES ('sail');
INSERT INTO all_verbs VALUES ('sally');
INSERT INTO all_verbs VALUES ('salute');
INSERT INTO all_verbs VALUES ('salvage');
INSERT INTO all_verbs VALUES ('salve');
INSERT INTO all_verbs VALUES ('sample');
INSERT INTO all_verbs VALUES ('sanctify');
INSERT INTO all_verbs VALUES ('sanction');
INSERT INTO all_verbs VALUES ('sap');
INSERT INTO all_verbs VALUES ('saponify');
INSERT INTO all_verbs VALUES ('sash');
INSERT INTO all_verbs VALUES ('sashay');
INSERT INTO all_verbs VALUES ('sass');
INSERT INTO all_verbs VALUES ('sate');
INSERT INTO all_verbs VALUES ('satiate');
INSERT INTO all_verbs VALUES ('satirise');
INSERT INTO all_verbs VALUES ('satisfy');
INSERT INTO all_verbs VALUES ('saturate');
INSERT INTO all_verbs VALUES ('saunter');
INSERT INTO all_verbs VALUES ('save');
INSERT INTO all_verbs VALUES ('savor');
INSERT INTO all_verbs VALUES ('savvy');
INSERT INTO all_verbs VALUES ('saw');
INSERT INTO all_verbs VALUES ('say');
INSERT INTO all_verbs VALUES ('scab');
INSERT INTO all_verbs VALUES ('scabble');
INSERT INTO all_verbs VALUES ('scald');
INSERT INTO all_verbs VALUES ('scale');
INSERT INTO all_verbs VALUES ('scam');
INSERT INTO all_verbs VALUES ('scan');
INSERT INTO all_verbs VALUES ('scant');
INSERT INTO all_verbs VALUES ('scar');
INSERT INTO all_verbs VALUES ('scare');
INSERT INTO all_verbs VALUES ('scarify');
INSERT INTO all_verbs VALUES ('scarp');
INSERT INTO all_verbs VALUES ('scat');
INSERT INTO all_verbs VALUES ('scatter');
INSERT INTO all_verbs VALUES ('scold');
INSERT INTO all_verbs VALUES ('scorch');
INSERT INTO all_verbs VALUES ('scowl');
INSERT INTO all_verbs VALUES ('scrawl');
INSERT INTO all_verbs VALUES ('scream');
INSERT INTO all_verbs VALUES ('screw');
INSERT INTO all_verbs VALUES ('scrub');
INSERT INTO all_verbs VALUES ('search');
INSERT INTO all_verbs VALUES ('seat');
INSERT INTO all_verbs VALUES ('secure');
INSERT INTO all_verbs VALUES ('see');
INSERT INTO all_verbs VALUES ('seek');
INSERT INTO all_verbs VALUES ('seem');
INSERT INTO all_verbs VALUES ('seize');
INSERT INTO all_verbs VALUES ('select');
INSERT INTO all_verbs VALUES ('sell');
INSERT INTO all_verbs VALUES ('send');
INSERT INTO all_verbs VALUES ('sentence');
INSERT INTO all_verbs VALUES ('separate');
INSERT INTO all_verbs VALUES ('set');
INSERT INTO all_verbs VALUES ('sever');
INSERT INTO all_verbs VALUES ('sew');
INSERT INTO all_verbs VALUES ('shake');
INSERT INTO all_verbs VALUES ('shape');
INSERT INTO all_verbs VALUES ('share');
INSERT INTO all_verbs VALUES ('shatter');
INSERT INTO all_verbs VALUES ('shave');
INSERT INTO all_verbs VALUES ('shear');
INSERT INTO all_verbs VALUES ('shed');
INSERT INTO all_verbs VALUES ('shine');
INSERT INTO all_verbs VALUES ('shirk');
INSERT INTO all_verbs VALUES ('shit');
INSERT INTO all_verbs VALUES ('shiver');
INSERT INTO all_verbs VALUES ('shock');
INSERT INTO all_verbs VALUES ('shoe');
INSERT INTO all_verbs VALUES ('shoot');
INSERT INTO all_verbs VALUES ('shorten');
INSERT INTO all_verbs VALUES ('shout');
INSERT INTO all_verbs VALUES ('show');
INSERT INTO all_verbs VALUES ('shrink');
INSERT INTO all_verbs VALUES ('shun');
INSERT INTO all_verbs VALUES ('shut');
INSERT INTO all_verbs VALUES ('sight');
INSERT INTO all_verbs VALUES ('signal');
INSERT INTO all_verbs VALUES ('signify');
INSERT INTO all_verbs VALUES ('sing');
INSERT INTO all_verbs VALUES ('sink');
INSERT INTO all_verbs VALUES ('sip');
INSERT INTO all_verbs VALUES ('sit');
INSERT INTO all_verbs VALUES ('ski');
INSERT INTO all_verbs VALUES ('skid');
INSERT INTO all_verbs VALUES ('slam');
INSERT INTO all_verbs VALUES ('slash');
INSERT INTO all_verbs VALUES ('slay');
INSERT INTO all_verbs VALUES ('sleep');
INSERT INTO all_verbs VALUES ('slide');
INSERT INTO all_verbs VALUES ('slim');
INSERT INTO all_verbs VALUES ('sling');
INSERT INTO all_verbs VALUES ('slink');
INSERT INTO all_verbs VALUES ('slip');
INSERT INTO all_verbs VALUES ('slit');
INSERT INTO all_verbs VALUES ('smash');
INSERT INTO all_verbs VALUES ('smell');
INSERT INTO all_verbs VALUES ('smile');
INSERT INTO all_verbs VALUES ('smite');
INSERT INTO all_verbs VALUES ('smooth');
INSERT INTO all_verbs VALUES ('smother');
INSERT INTO all_verbs VALUES ('snap');
INSERT INTO all_verbs VALUES ('snatch');
INSERT INTO all_verbs VALUES ('sneak');
INSERT INTO all_verbs VALUES ('sneeze');
INSERT INTO all_verbs VALUES ('sniff');
INSERT INTO all_verbs VALUES ('soar');
INSERT INTO all_verbs VALUES ('sob');
INSERT INTO all_verbs VALUES ('solicit');
INSERT INTO all_verbs VALUES ('solve');
INSERT INTO all_verbs VALUES ('soothe');
INSERT INTO all_verbs VALUES ('sort');
INSERT INTO all_verbs VALUES ('sow');
INSERT INTO all_verbs VALUES ('sparkle');
INSERT INTO all_verbs VALUES ('speak');
INSERT INTO all_verbs VALUES ('speed');
INSERT INTO all_verbs VALUES ('spell');
INSERT INTO all_verbs VALUES ('spend');
INSERT INTO all_verbs VALUES ('spill');
INSERT INTO all_verbs VALUES ('spin');
INSERT INTO all_verbs VALUES ('spit');
INSERT INTO all_verbs VALUES ('split');
INSERT INTO all_verbs VALUES ('spoil');
INSERT INTO all_verbs VALUES ('spray');
INSERT INTO all_verbs VALUES ('spread');
INSERT INTO all_verbs VALUES ('spring');
INSERT INTO all_verbs VALUES ('sprout');
INSERT INTO all_verbs VALUES ('squeeze');
INSERT INTO all_verbs VALUES ('stand');
INSERT INTO all_verbs VALUES ('stare');
INSERT INTO all_verbs VALUES ('start');
INSERT INTO all_verbs VALUES ('state');
INSERT INTO all_verbs VALUES ('stay');
INSERT INTO all_verbs VALUES ('steal');
INSERT INTO all_verbs VALUES ('steep');
INSERT INTO all_verbs VALUES ('stem');
INSERT INTO all_verbs VALUES ('step');
INSERT INTO all_verbs VALUES ('sterilize');
INSERT INTO all_verbs VALUES ('stick');
INSERT INTO all_verbs VALUES ('stimulate');
INSERT INTO all_verbs VALUES ('sting');
INSERT INTO all_verbs VALUES ('stink');
INSERT INTO all_verbs VALUES ('stir');
INSERT INTO all_verbs VALUES ('stitch');
INSERT INTO all_verbs VALUES ('stoop');
INSERT INTO all_verbs VALUES ('stop');
INSERT INTO all_verbs VALUES ('store');
INSERT INTO all_verbs VALUES ('strain');
INSERT INTO all_verbs VALUES ('stray');
INSERT INTO all_verbs VALUES ('stress');
INSERT INTO all_verbs VALUES ('stretch');
INSERT INTO all_verbs VALUES ('strew');
INSERT INTO all_verbs VALUES ('stride');
INSERT INTO all_verbs VALUES ('strike');
INSERT INTO all_verbs VALUES ('string');
INSERT INTO all_verbs VALUES ('strive');
INSERT INTO all_verbs VALUES ('study');
INSERT INTO all_verbs VALUES ('submit');
INSERT INTO all_verbs VALUES ('subscribe');
INSERT INTO all_verbs VALUES ('subtract');
INSERT INTO all_verbs VALUES ('succeed');
INSERT INTO all_verbs VALUES ('suck');
INSERT INTO all_verbs VALUES ('suffer');
INSERT INTO all_verbs VALUES ('suggest');
INSERT INTO all_verbs VALUES ('summon');
INSERT INTO all_verbs VALUES ('supply');
INSERT INTO all_verbs VALUES ('support');
INSERT INTO all_verbs VALUES ('suppose');
INSERT INTO all_verbs VALUES ('surge');
INSERT INTO all_verbs VALUES ('surmise');
INSERT INTO all_verbs VALUES ('surpass');
INSERT INTO all_verbs VALUES ('surround');
INSERT INTO all_verbs VALUES ('survey');
INSERT INTO all_verbs VALUES ('survive');
INSERT INTO all_verbs VALUES ('swallow');
INSERT INTO all_verbs VALUES ('sway');
INSERT INTO all_verbs VALUES ('swear');
INSERT INTO all_verbs VALUES ('sweat');
INSERT INTO all_verbs VALUES ('sweep');
INSERT INTO all_verbs VALUES ('swell');
INSERT INTO all_verbs VALUES ('swim');
INSERT INTO all_verbs VALUES ('swing');
INSERT INTO all_verbs VALUES ('swot');
INSERT INTO all_verbs VALUES ('take');
INSERT INTO all_verbs VALUES ('talk');
INSERT INTO all_verbs VALUES ('tap');
INSERT INTO all_verbs VALUES ('taste');
INSERT INTO all_verbs VALUES ('tax');
INSERT INTO all_verbs VALUES ('teach');
INSERT INTO all_verbs VALUES ('tear');
INSERT INTO all_verbs VALUES ('tee');
INSERT INTO all_verbs VALUES ('tell');
INSERT INTO all_verbs VALUES ('tempt');
INSERT INTO all_verbs VALUES ('tend');
INSERT INTO all_verbs VALUES ('terminate');
INSERT INTO all_verbs VALUES ('terrify');
INSERT INTO all_verbs VALUES ('test');
INSERT INTO all_verbs VALUES ('thank');
INSERT INTO all_verbs VALUES ('think');
INSERT INTO all_verbs VALUES ('thrive');
INSERT INTO all_verbs VALUES ('throw');
INSERT INTO all_verbs VALUES ('thrust');
INSERT INTO all_verbs VALUES ('thump');
INSERT INTO all_verbs VALUES ('tie');
INSERT INTO all_verbs VALUES ('tire');
INSERT INTO all_verbs VALUES ('toss');
INSERT INTO all_verbs VALUES ('touch');
INSERT INTO all_verbs VALUES ('train');
INSERT INTO all_verbs VALUES ('trample');
INSERT INTO all_verbs VALUES ('transfer');
INSERT INTO all_verbs VALUES ('transform');
INSERT INTO all_verbs VALUES ('translate');
INSERT INTO all_verbs VALUES ('trap');
INSERT INTO all_verbs VALUES ('travel');
INSERT INTO all_verbs VALUES ('tread');
INSERT INTO all_verbs VALUES ('treasure');
INSERT INTO all_verbs VALUES ('treat');
INSERT INTO all_verbs VALUES ('tree');
INSERT INTO all_verbs VALUES ('tremble');
INSERT INTO all_verbs VALUES ('triumph');
INSERT INTO all_verbs VALUES ('trust');
INSERT INTO all_verbs VALUES ('try');
INSERT INTO all_verbs VALUES ('turn');
INSERT INTO all_verbs VALUES ('type');
INSERT INTO all_verbs VALUES ('typeset');
INSERT INTO all_verbs VALUES ('understand');
INSERT INTO all_verbs VALUES ('undo');
INSERT INTO all_verbs VALUES ('uproot');
INSERT INTO all_verbs VALUES ('upset');
INSERT INTO all_verbs VALUES ('urge');
INSERT INTO all_verbs VALUES ('use');
INSERT INTO all_verbs VALUES ('utter');
INSERT INTO all_verbs VALUES ('value');
INSERT INTO all_verbs VALUES ('vanish');
INSERT INTO all_verbs VALUES ('vary');
INSERT INTO all_verbs VALUES ('verify');
INSERT INTO all_verbs VALUES ('vex');
INSERT INTO all_verbs VALUES ('vie');
INSERT INTO all_verbs VALUES ('view');
INSERT INTO all_verbs VALUES ('violate');
INSERT INTO all_verbs VALUES ('vomit');
INSERT INTO all_verbs VALUES ('wake');
INSERT INTO all_verbs VALUES ('walk');
INSERT INTO all_verbs VALUES ('wander');
INSERT INTO all_verbs VALUES ('want');
INSERT INTO all_verbs VALUES ('warn');
INSERT INTO all_verbs VALUES ('waste');
INSERT INTO all_verbs VALUES ('watch');
INSERT INTO all_verbs VALUES ('water');
INSERT INTO all_verbs VALUES ('wave');
INSERT INTO all_verbs VALUES ('wax');
INSERT INTO all_verbs VALUES ('waylay');
INSERT INTO all_verbs VALUES ('wear');
INSERT INTO all_verbs VALUES ('weave');
INSERT INTO all_verbs VALUES ('wed');
INSERT INTO all_verbs VALUES ('weep');
INSERT INTO all_verbs VALUES ('weigh');
INSERT INTO all_verbs VALUES ('welcome');
INSERT INTO all_verbs VALUES ('wend');
INSERT INTO all_verbs VALUES ('wet');
INSERT INTO all_verbs VALUES ('whip');
INSERT INTO all_verbs VALUES ('whisper');
INSERT INTO all_verbs VALUES ('win');
INSERT INTO all_verbs VALUES ('wind');
INSERT INTO all_verbs VALUES ('wish');
INSERT INTO all_verbs VALUES ('withdraw');
INSERT INTO all_verbs VALUES ('work');
INSERT INTO all_verbs VALUES ('worry');
INSERT INTO all_verbs VALUES ('worship');
INSERT INTO all_verbs VALUES ('wring');
INSERT INTO all_verbs VALUES ('write');
INSERT INTO all_verbs VALUES ('yawn');
INSERT INTO all_verbs VALUES ('yell');
INSERT INTO all_verbs VALUES ('yield');
INSERT INTO all_verbs VALUES ('zinc');
INSERT INTO all_verbs VALUES ('zoom');