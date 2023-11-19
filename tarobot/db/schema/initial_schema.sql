-- create the schema, associated user, and grant schema privs to that user
CREATE DATABASE `${DB_SCHEMA_NAME}`;
CREATE USER '${DB_SCHEMA_USER}'@'${DB_SCHEMA_HOST}' IDENTIFIED WITH mysql_native_password BY '${DB_SCHEMA_PASS}';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, INDEX, DROP, ALTER, CREATE TEMPORARY TABLES, LOCK TABLES
    ON `${DB_SCHEMA_NAME}`.* TO '${DB_SCHEMA_USER}'@'${DB_SCHEMA_HOST}';
USE `${DB_SCHEMA_NAME}`;

-- create tables
CREATE TABLE `card`(
    `ordinal` TINYINT NOT NULL,
    `name` VARCHAR(32) NOT NULL,
    `is_major` TINYINT,
    `suit` VARCHAR(16),
    `rank` TINYINT(1),
    PRIMARY KEY (ordinal)
);

CREATE TABLE `reading`(
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `openai_id` VARCHAR(64) NOT NULL,
    `card_one` TINYINT NOT NULL,
    `card_two` TINYINT,
    `card_three` TINYINT,
    `card_four` TINYINT,
    `card_five` TINYINT,
    `parameters` VARCHAR(256),
    `prompt` VARCHAR(1024) NOT NULL,
    `response` TEXT NOT NULL,
    `summary` VARCHAR(64),
    `model` VARCHAR(64),
    `created_ts` TIMESTAMP,
    `response_ms` INT,
    `max_tokens` INT,
    `prompt_tokens` INT,
    `completion_tokens` INT,
    `total_tokens` INT,
    `temperature` FLOAT,
    `top_p` FLOAT,
    PRIMARY KEY (`id`),
    FOREIGN KEY `idx_card_one` (`card_one`) REFERENCES `card`(`ordinal`),
    FOREIGN KEY `idx_card_two` (`card_two`) REFERENCES `card`(`ordinal`),
    FOREIGN KEY `idx_card_three` (`card_three`) REFERENCES `card`(`ordinal`),
    FOREIGN KEY `idx_card_four` (`card_four`) REFERENCES `card`(`ordinal`),
    FOREIGN KEY `idx_card_five` (`card_five`) REFERENCES `card`(`ordinal`)
);

-- populate tarot card table
INSERT INTO `card`(`ordinal`, `name`) VALUES(0, 'The Fool');
INSERT INTO `card`(`ordinal`, `name`) VALUES(1, 'The Magician');
INSERT INTO `card`(`ordinal`, `name`) VALUES(2, 'The High Priestess');
INSERT INTO `card`(`ordinal`, `name`) VALUES(3, 'The Empress');
INSERT INTO `card`(`ordinal`, `name`) VALUES(4, 'The Emperor');
INSERT INTO `card`(`ordinal`, `name`) VALUES(5, 'The Hierophant');
INSERT INTO `card`(`ordinal`, `name`) VALUES(6, 'The Lovers');
INSERT INTO `card`(`ordinal`, `name`) VALUES(7, 'The Chariot');
INSERT INTO `card`(`ordinal`, `name`) VALUES(8, 'Justice');
INSERT INTO `card`(`ordinal`, `name`) VALUES(9, 'The Hermit');
INSERT INTO `card`(`ordinal`, `name`) VALUES(10, 'The Wheel of Fortune');
INSERT INTO `card`(`ordinal`, `name`) VALUES(11, 'Strength');
INSERT INTO `card`(`ordinal`, `name`) VALUES(12, 'The Hanged Man');
INSERT INTO `card`(`ordinal`, `name`) VALUES(13, 'Death');
INSERT INTO `card`(`ordinal`, `name`) VALUES(14, 'Temperance');
INSERT INTO `card`(`ordinal`, `name`) VALUES(15, 'The Devil');
INSERT INTO `card`(`ordinal`, `name`) VALUES(16, 'The Tower');
INSERT INTO `card`(`ordinal`, `name`) VALUES(17, 'The Star');
INSERT INTO `card`(`ordinal`, `name`) VALUES(18, 'The Moon');
INSERT INTO `card`(`ordinal`, `name`) VALUES(19, 'The Sun');
INSERT INTO `card`(`ordinal`, `name`) VALUES(20, 'Judgement');
INSERT INTO `card`(`ordinal`, `name`) VALUES(21, 'The World');
INSERT INTO `card`(`ordinal`, `name`) VALUES(22, 'Ace of Wands');
INSERT INTO `card`(`ordinal`, `name`) VALUES(23, 'Two of Wands');
INSERT INTO `card`(`ordinal`, `name`) VALUES(24, 'Three of Wands');
INSERT INTO `card`(`ordinal`, `name`) VALUES(25, 'Four of Wands');
INSERT INTO `card`(`ordinal`, `name`) VALUES(26, 'Five of Wands');
INSERT INTO `card`(`ordinal`, `name`) VALUES(27, 'Six of Wands');
INSERT INTO `card`(`ordinal`, `name`) VALUES(28, 'Seven of Wands');
INSERT INTO `card`(`ordinal`, `name`) VALUES(29, 'Eight of Wands');
INSERT INTO `card`(`ordinal`, `name`) VALUES(30, 'Nine of Wands');
INSERT INTO `card`(`ordinal`, `name`) VALUES(31, 'Ten of Wands');
INSERT INTO `card`(`ordinal`, `name`) VALUES(32, 'Page of Wands');
INSERT INTO `card`(`ordinal`, `name`) VALUES(33, 'Knight of Wands');
INSERT INTO `card`(`ordinal`, `name`) VALUES(34, 'Queen of Wands');
INSERT INTO `card`(`ordinal`, `name`) VALUES(35, 'King of Wands');
INSERT INTO `card`(`ordinal`, `name`) VALUES(36, 'Ace of Cups');
INSERT INTO `card`(`ordinal`, `name`) VALUES(37, 'Two of Cups');
INSERT INTO `card`(`ordinal`, `name`) VALUES(38, 'Three of Cups');
INSERT INTO `card`(`ordinal`, `name`) VALUES(39, 'Four of Cups');
INSERT INTO `card`(`ordinal`, `name`) VALUES(40, 'Five of Cups');
INSERT INTO `card`(`ordinal`, `name`) VALUES(41, 'Six of Cups');
INSERT INTO `card`(`ordinal`, `name`) VALUES(42, 'Seven of Cups');
INSERT INTO `card`(`ordinal`, `name`) VALUES(43, 'Eight of Cups');
INSERT INTO `card`(`ordinal`, `name`) VALUES(44, 'Nine of Cups');
INSERT INTO `card`(`ordinal`, `name`) VALUES(45, 'Ten of Cups');
INSERT INTO `card`(`ordinal`, `name`) VALUES(46, 'Page of Cups');
INSERT INTO `card`(`ordinal`, `name`) VALUES(47, 'Knight of Cups');
INSERT INTO `card`(`ordinal`, `name`) VALUES(48, 'Queen of Cups');
INSERT INTO `card`(`ordinal`, `name`) VALUES(49, 'King of Cups');
INSERT INTO `card`(`ordinal`, `name`) VALUES(50, 'Ace of Swords');
INSERT INTO `card`(`ordinal`, `name`) VALUES(51, 'Two of Swords');
INSERT INTO `card`(`ordinal`, `name`) VALUES(52, 'Three of Swords');
INSERT INTO `card`(`ordinal`, `name`) VALUES(53, 'Four of Swords');
INSERT INTO `card`(`ordinal`, `name`) VALUES(54, 'Five of Swords');
INSERT INTO `card`(`ordinal`, `name`) VALUES(55, 'Six of Swords');
INSERT INTO `card`(`ordinal`, `name`) VALUES(56, 'Seven of Swords');
INSERT INTO `card`(`ordinal`, `name`) VALUES(57, 'Eight of Swords');
INSERT INTO `card`(`ordinal`, `name`) VALUES(58, 'Nine of Swords');
INSERT INTO `card`(`ordinal`, `name`) VALUES(59, 'Ten of Swords');
INSERT INTO `card`(`ordinal`, `name`) VALUES(60, 'Page of Swords');
INSERT INTO `card`(`ordinal`, `name`) VALUES(61, 'Knight of Swords');
INSERT INTO `card`(`ordinal`, `name`) VALUES(62, 'Queen of Swords');
INSERT INTO `card`(`ordinal`, `name`) VALUES(63, 'King of Swords');
INSERT INTO `card`(`ordinal`, `name`) VALUES(64, 'Ace of Pentacles');
INSERT INTO `card`(`ordinal`, `name`) VALUES(65, 'Two of Pentacles');
INSERT INTO `card`(`ordinal`, `name`) VALUES(66, 'Three of Pentacles');
INSERT INTO `card`(`ordinal`, `name`) VALUES(67, 'Four of Pentacles');
INSERT INTO `card`(`ordinal`, `name`) VALUES(68, 'Five of Pentacles');
INSERT INTO `card`(`ordinal`, `name`) VALUES(69, 'Six of Pentacles');
INSERT INTO `card`(`ordinal`, `name`) VALUES(70, 'Seven of Pentacles');
INSERT INTO `card`(`ordinal`, `name`) VALUES(71, 'Eight of Pentacles');
INSERT INTO `card`(`ordinal`, `name`) VALUES(72, 'Nine of Pentacles');
INSERT INTO `card`(`ordinal`, `name`) VALUES(73, 'Ten of Pentacles');
INSERT INTO `card`(`ordinal`, `name`) VALUES(74, 'Page of Pentacles');
INSERT INTO `card`(`ordinal`, `name`) VALUES(75, 'Knight of Pentacles');
INSERT INTO `card`(`ordinal`, `name`) VALUES(76, 'Queen of Pentacles');
INSERT INTO `card`(`ordinal`, `name`) VALUES(77, 'King of Pentacles');

-- sets flag for minor/major archana for each card
UPDATE `card` SET `is_major` = 0 WHERE `ordinal` >= 22;
UPDATE `card` SET `is_major` = 1 WHERE `ordinal` < 22;

-- set the suit name for all minor archana cards
UPDATE `card` SET `suit` = 'Wands' WHERE `ordinal` BETWEEN 22 AND 35;
UPDATE `card` SET `suit` = 'Cups' WHERE `ordinal` BETWEEN 36 AND 49;
UPDATE `card` SET `suit` = 'Swords' WHERE `ordinal` BETWEEN 50 AND 63;
UPDATE `card` SET `suit` = 'Pentacles' WHERE `ordinal` BETWEEN 64 AND 77;

-- sets the card value for each minor archana card: 1 (ace), 2, 3 .. 10, 11 (page), 12 (knight), 13 (queen), 14 (king)
UPDATE `card` SET `rank` = ((`ordinal` - 22) % 14 + 1) WHERE `ordinal` > 21;
