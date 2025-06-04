CREATE TYPE equipment_slot AS ENUM (
    'head', 'neck', 'shoulders', 'chest', 'back', 'wrists',
    'hands', 'waist', 'legs', 'feet', 'finger_1', 'finger_2',
    'trinket_1', 'trinket_2', 'main_hand', 'off_hand', 'tabard', 'shirt');
CREATE TYPE role_type AS ENUM ('tank', 'dps', 'healer');
CREATE TYPE gender_type AS ENUM ('male', 'female');
CREATE TYPE item_quality AS ENUM ('common', 'uncommon', 'rare', 'epic', 'legendary', 'artifact');
CREATE TYPE item_class AS ENUM ('weapon', 'armor', 'consumable', 'trade_goods', 'quest_item', 'container');
CREATE TYPE binding_type AS ENUM ('BoP', 'BoE', 'BtA');
CREATE TYPE objective_type AS ENUM ('kill','collect','use');
CREATE TYPE character_reputation_level AS ENUM ('hated', 'hostile', 'unfriendly', 'neutral',
            'friendly', 'honored', 'revered', 'exalted');
CREATE TYPE player_rank_type AS ENUM ('recruit', 'participant', 'veteran', 'officer', 'guild master');
CREATE TYPE item_state_type AS ENUM ('Intellect', 'Agility', 'Strength', 'Stamina', 'Armor', 'Critical Strike Chance',
 'Haste', 'Mastery', 'Versatility', 'Speed', 'Leech', 'Avoidance');
CREATE TYPE character_quest_status AS ENUM ('active', 'completed', 'failed');


CREATE TABLE location (
    id UUID PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    expansion_id UUID NOT NULL REFERENCES expansion(id)
);

CREATE TABLE race (
    id UUID PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    starting_zone_id UUID NOT NULL REFERENCES location(id)
);

CREATE TABLE specialization (
    id UUID PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    class_id UUID NOT NULL REFERENCES class(id),
    role role_type NOT NULL
);

CREATE TABLE game_character (
    id UUID PRIMARY KEY,
    account_id UUID NOT NULL REFERENCES account(id),
    name VARCHAR(12) UNIQUE NOT NULL,
    gender gender_type NOT NULL,
    race_id UUID NOT NULL REFERENCES race(id),
    class_id UUID NOT NULL REFERENCES class(id),
    spec_id UUID NOT NULL REFERENCES specialization(id),
    server_id UUID NOT NULL REFERENCES server(id),
    expansion_id UUID NOT NULL REFERENCES expansion(id),
    location_id UUID NOT NULL REFERENCES location(id),
    gold INT DEFAULT 0 NOT NULL CHECK (gold > -1),
    silver INT DEFAULT 0 NOT NULL CHECK (silver > -1),
    copper INT DEFAULT 0 NOT NULL CHECK (copper > -1),
    total_playtime INTERVAL NOT NULL,
    total_exp_gained INT DEFAULT 0 NOT NULL CHECK (total_exp_gained > -1)
);

CREATE TABLE item (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    item_level INT NOT NULL CHECK (item_level > 0),
    quality item_quality NOT NULL,
    max_stack INT DEFAULT 1 NOT NULL CHECK (max_stack > 0),
    gold INT DEFAULT 0 NOT NULL CHECK (gold > -1),
    silver INT DEFAULT 0 NOT NULL CHECK (silver > -1),
    copper INT DEFAULT 0 NOT NULL CHECK (copper > -1),
    description TEXT NOT NULL,
    expansion_id UUID NOT NULL REFERENCES expansion(id),
    item_class item_class NOT NULL,
    binding_type binding_type NOT NULL,
    required_level INT DEFAULT 0 NOT NULL CHECK (required_level > -1)
);

CREATE TABLE armor (
    id UUID PRIMARY KEY NOT NULL REFERENCES item(id),
    durability INT CHECK (durability IS NULL OR durability > 0), -- прочность предмета, если NULL - то предмет не теряет прочность
    armor_type VARCHAR(16) NOT NULL,
    armor_value INT NOT NULL CHECK (armor_value > -1),
    slot equipment_slot NOT NULL
);

CREATE TABLE weapon (
    id UUID PRIMARY KEY NOT NULL REFERENCES item(id),
    durability INT CHECK (durability IS NULL OR durability > 0),
    damage_min INT NOT NULL CHECK (damage_min > 0),
    damage_max INT NOT NULL CHECK (damage_max > 0),
    attack_speed FLOAT NOT NULL CHECK (attack_speed > 0),
    weapon_type VARCHAR(32) NOT NULL,
    handedness VARCHAR(16) NOT NULL
);

CREATE TABLE consumable (
    id UUID PRIMARY KEY NOT NULL REFERENCES item(id),
    effect VARCHAR(32) NOT NULL,
    duration INT NOT NULL CHECK (duration > 0),
    cooldown INT NOT NULL CHECK (duration > -1),
    charges INT NOT NULL DEFAULT 1 CHECK (charges > 0),
    required_level INT NOT NULL DEFAULT 0 CHECK (required_level > -1)
);

CREATE TABLE trade_goods (
    id UUID PRIMARY KEY NOT NULL REFERENCES item(id),
    profession_id UUID NOT NULL REFERENCES profession(id)
);

CREATE TABLE quest_item (
    id UUID NOT NULL PRIMARY KEY REFERENCES item(id),
    quest_id UUID NOT NULL REFERENCES quest(id),
    is_quest_start BOOLEAN NOT NULL
);

CREATE TABLE container (
    id UUID NOT NULL PRIMARY KEY REFERENCES item(id),
    container_size INT NOT NULL CHECK (container_size > 0)
);

CREATE TABLE recipe (
  id UUID PRIMARY KEY,
  name VARCHAR(128) NOT NULL,
  expansion_id UUID NOT NULL REFERENCES expansion(id),
  profession_id UUID NOT NULL REFERENCES profession(id),
  result_item_id UUID NOT NULL REFERENCES item(id),
  required_skill INT NOT NULL DEFAULT 0 CHECK (required_skill > -1)
);

CREATE TABLE mob (
  id UUID PRIMARY KEY,
  name VARCHAR(64) NOT NULL,
  location_id UUID NOT NULL REFERENCES location(id),
  is_boss BOOLEAN NOT NULL,
  level_mob INT NOT NULL CHECK (level_mob > 0)
);

CREATE TABLE objective (
  id UUID PRIMARY KEY,
  type objective_type NOT NULL,
  target_mob_id UUID REFERENCES mob(id),
  target_item_id UUID REFERENCES item(id),
  quantity INT NOT NULL CHECK (quantity > 0),
  quest_id UUID NOT NULL REFERENCES quest(id),
  CONSTRAINT chk_objective_type
    CHECK (
        (type = 'kill' AND target_mob_id IS NOT NULL AND target_item_id IS NULL) OR
        (type = 'collect' AND target_item_id IS NOT NULL AND target_mob_id IS NULL) OR
        (type = 'use' AND target_mob_id IS NULL AND target_item_id IS NULL)
    )
);

CREATE TABLE dungeon (
  id UUID PRIMARY KEY,
  name VARCHAR(64) UNIQUE NOT NULL,
  location_id UUID NOT NULL REFERENCES location(id),
  expansion_id UUID NOT NULL REFERENCES expansion(id)
);

CREATE TABLE raid (
  id UUID PRIMARY KEY,
  name VARCHAR(64) UNIQUE NOT NULL,
  location_id UUID NOT NULL REFERENCES location(id),
  expansion_id UUID NOT NULL REFERENCES expansion(id)
);

CREATE TABLE currency (
  id UUID PRIMARY KEY,
  name VARCHAR(64) UNIQUE NOT NULL,
  expansion_id UUID NOT NULL REFERENCES expansion(id)
);

CREATE TABLE reputation (
  id UUID PRIMARY KEY,
  name VARCHAR(64) UNIQUE NOT NULL,
  expansion_id UUID NOT NULL REFERENCES expansion(id)
);

CREATE TABLE writing (
  id UUID PRIMARY KEY,
  sender_id UUID NOT NULL REFERENCES game_character(id),
  recipient_id UUID NOT NULL REFERENCES game_character(id),
  subject VARCHAR(40) NOT NULL,
  body TEXT,
  gold INT NOT NULL DEFAULT 0 CHECK (gold > -1),
  silver INT NOT NULL DEFAULT 0 CHECK (silver > -1),
  copper INT NOT NULL DEFAULT 0 CHECK (copper > -1),
  cod BOOLEAN NOT NULL,
  expires_at TIMESTAMP NOT NULL
);

CREATE TABLE auction_lot (
  id UUID PRIMARY KEY,
  character_id UUID NOT NULL REFERENCES game_character(id),
  item_id UUID NOT NULL REFERENCES item(id),
  quantity INT NOT NULL DEFAULT 1 CHECK (quantity > 0),
  gold INT NOT NULL CHECK (gold > -1),
  silver INT NOT NULL CHECK (silver > -1),
  copper INT NOT NULL CHECK (copper > -1),
  buyout_mode BOOLEAN NOT NULL,
  expires_at TIMESTAMP NOT NULL
);

-- 20