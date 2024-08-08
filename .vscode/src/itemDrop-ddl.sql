# itemDrop-ddl.sql


# Drops all tables.

SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS game;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS NPC;
DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS has;
DROP TABLE IF EXISTS ground_drop_at;
DROP TABLE IF EXISTS located;
# ... 
SET FOREIGN_KEY_CHECKS=1;

CREATE TABLE game (
    game_id int NOT NULL,
    game_name varchar(255) NOT NULL,
    game_version varchar(255) NOT NULL,
    game_genre varchar(255) NOT NULL,
    PRIMARY KEY(game_id)
);

INSERT INTO game ( game_id, game_name, game_version, game_genre) values 
    (5001, 'Skyrim', '1.0', 'RPG'),
    (5002, 'Minecraft', '1.17', 'Sandbox'),
    (5003, 'Call of Duty', '5.2', 'FPS'),
    (5004, 'The Legend of Zelda: Breath of the Wild', '2.1', 'Adventure'),
    (5005, 'Among Us', '2.0', 'Social Deduction'),
    (5006, 'Fornite', '13.0', 'Battle Royale'),
    (5007, 'Civilization VI', '1.6', 'Strategy'),
    (5008, 'Overwatch', '4.0', 'FPS'),
    (5009, 'Stardew Valley', '1.5', 'Simulation'),
    (5010, 'Dark Souls', '3.1', 'Action RPG');
    

CREATE TABLE locations (
    location_id int NOT NULL,
    location_name varchar(255) NOT NULL,
    location_level int,
    game_id int NOT NULL,
    PRIMARY KEY (location_id),
    CONSTRAINT FK_Game_id FOREIGN KEY (game_id) REFERENCES game(game_id) ON DELETE CASCADE
);

insert into locations (location_id, location_name, location_level, game_id) values 
    (3001, 'Village', 1, 5001),
    (3002, 'Forest', 2, 5002),
    (3003, 'Caves', 3, 5003),
    (3004, 'Castle', 4, 5004),
    (3005, 'Desert', 5, 5005),
    (3006, 'Mountains', 6, 5006),
    (3007, 'Swamp', 7, 5007),
    (3008, 'Ruins', 8, 5008),
    (3009, 'Underworld', 9, 5009),
    (3010, 'Sky City', 10, 5010);

CREATE TABLE item (
    item_id int NOT NULL,
    item_name varchar(255) NOT NULL,
    item_type varchar(255) NOT NULL,
    item_def int,
    item_atk int, 
    item_recipe varchar(4096),
    item_effect varchar(4096),
    PRIMARY KEY(item_id)
);

INSERT INTO item (item_id, item_name, item_type, item_def, item_atk, item_recipe, item_effect) values 
    (2001, 'Iron Sword', 'Weapon', 0, 10, 'None', 'None'),
    (2002, 'Wooden Shield', 'Shield', 15, 0, 'None', 'None'),
    (2003, 'Health Potion', 'Potion', 0, 0, 'None', 'Restore 50 HP'),
    (2004, 'Steel Armor', 'Armor', 30, 0, 'None', 'None'),
    (2005, 'Fire Scroll', 'Scroll', 0, 0, 'None', 'Casts Fireball Spell'),
    (2006, 'Health Elixir', 'Potion', 0, 0, 'None', 'Restore all HP/MP'),
    (2007, 'Diamon Dagger', 'Weapon', 0, 18, 'None', 'None'),
    (2008, 'Potion of Invisibility', 'Potion', 0, 0, 'None', 'Grants Invisibility for 30 seconds'),
    (2009, 'Leather Helmet', 'Helmet', 10, 0, 'None', 'None'),
    (2010, 'Magic Wand', 'Staff', 0, 5, 'Wooden Stick, Magic Crystal', 'None');

CREATE TABLE NPC (
    NPC_id int NOT NULL,
    NPC_lv int NOT NULL,
    NPC_name varchar(255) NOT NULL,
    NPC_type varchar(255) NOT NULL,
    item_id int,
    PRIMARY KEY (NPC_id),
    CONSTRAINT FK_item_id FOREIGN KEY (item_id) REFERENCES item(item_id)  ON DELETE CASCADE
);

INSERT INTO NPC (NPC_id, NPC_lv, NPC_name, NPC_type, item_id) values 
    (1001, 1, 'Goblin Warrior', 'Hostile', 2001),
    (1002, 3, 'Tavern Keeper', 'Character', 2002),
    (1003, 2, 'Orc Shaman', 'Hostile', 2005),
    (1004, 5, 'Elder Druid', 'Character', 2006),
    (1005, 1, 'Bandit', 'Hostile', 2007),
    (1006, 4, 'Priestess Elara', 'Character', 2008),
    (1007, 6, 'Troll Berserker', 'Hostile', 2004),
    (1008, 2, 'Shopkeeper', 'Character', 2009),
    (1009, 3, 'Vampire Lord', 'Hostile', 2003),
    (1010, 7, 'King Arthur', 'Character', 2010);


CREATE TABLE player (
    player_id int NOT NULL,
    player_name varchar(255) NOT NULL,
    player_level int NOT NULL,
    PRIMARY KEY (player_id)
);

INSERT INTO player (player_id, player_name, player_level) values 
    (4001, 'John', 15),
    (4002, 'Sarah', 20),
    (4003, 'Michael', 12),
    (4004, 'Emily', 18),
    (4005, 'Robert', 7),
    (4006, 'Lisa', 22),
    (4007, 'Devid', 10),
    (4008, 'Jessica', 25),
    (4009, 'Kevin', 14),
    (4010, 'Mary', 9);


CREATE TABLE has (
    player_id int NOT NULL,
    item_id int NOT NULL,
    CONSTRAINT FK_player_id FOREIGN KEY (player_id) REFERENCES player(player_id)  ON DELETE CASCADE,
    CONSTRAINT FK_has_item_id FOREIGN KEY (item_id) REFERENCES item(item_id)  ON DELETE CASCADE
);

INSERT INTO has(player_id, item_id) values 
    (4001, 2002),
    (4001, 2003),
    (4002, 2002),
    (4002, 2004),
    (4003, 2002),
    (4003, 2004),
    (4004, 2006);

CREATE TABLE ground_drop_at (
    item_id int NOT NULL,
    location_id int NOT NULL,
    CONSTRAINT FK_ground_item_id FOREIGN KEY (item_id) REFERENCES item(item_id)  ON DELETE CASCADE,
    CONSTRAINT FK_ground_location_id FOREIGN KEY (location_id) REFERENCES locations(location_id)  ON DELETE CASCADE
);

INSERT INTO ground_drop_at(item_id, location_id) values 
    (2001, 3004),
    (2001, 3007),
    (2004, 3008),
    (2006, 3001),
    (2006, 3009),
    (2008, 3002);

CREATE TABLE located (
    NPC_id int NOT NULL,
    location_id int NOT NULL,
    CONSTRAINT FK_located_NPC_id FOREIGN KEY (NPC_id) REFERENCES NPC(NPC_id) ON DELETE CASCADE,
    CONSTRAINT FK_located_location_id FOREIGN KEY (location_id) REFERENCES locations(location_id) ON DELETE CASCADE
);

INSERT INTO located(NPC_id, location_id) values 
    (1001, 3004),
    (1001, 3007),
    (1004, 3008),
    (1006, 3001),
    (1006, 3009),
    (1008, 3002),
    (1007, 3003),
    (1002, 3005),
    (1003, 3010),
    (1005, 3006),
    (1009, 3008),
    (1010, 3001);