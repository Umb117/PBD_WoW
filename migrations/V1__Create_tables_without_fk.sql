CREATE TYPE subscription_status AS ENUM ('active', 'inactive');
CREATE TYPE mount_type AS ENUM ('flying', 'ground', 'aquatic');
CREATE TYPE pet_quality AS ENUM ('poor', 'common', 'uncommon', 'rare');
CREATE TYPE guild_type AS ENUM ('PvE', 'PvP', 'RP', 'mixed');
CREATE TYPE ability_type AS ENUM ('active', 'passive');
CREATE TYPE ability_resource AS ENUM ('mana', 'energy', 'rage', 'combo_points');
CREATE TYPE region_type AS ENUM ('EU', 'US', 'ASIA');
CREATE TYPE pet_type AS ENUM ('humanoid', 'beast', 'aquatic', 'magical',
               'mechanical', 'dragonkin', 'undead', 'elemental', 'flying');


CREATE TABLE account (
    id UUID PRIMARY KEY,
    username VARCHAR(12) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    second_name VARCHAR(100) NOT NULL,
    birth_date DATE NOT NULL,
    country_code CHAR(2) NOT NULL,
    subscription_status subscription_status,
    subscription_end TIMESTAMP
    CHECK (
        (subscription_status = 'active' AND subscription_end IS NOT NULL)
        OR
        (subscription_status = 'inactive' AND subscription_end IS NULL )
    )
);

CREATE TABLE server (
    id UUID PRIMARY KEY,
    name VARCHAR(64) UNIQUE NOT NULL,
    region region_type NOT NULL
);

CREATE TABLE expansion (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    min_level INT NOT NULL CHECK (min_level > -1),
    max_level INT NOT NULL CHECK (max_level > -1)
);

CREATE TABLE class (
    id UUID PRIMARY KEY,
    name VARCHAR(32) NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE ability (
    id UUID PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    description TEXT NOT NULL,
    type ability_type NOT NULL,
    cast_time FLOAT,
    resource ability_resource,
    range FLOAT NOT NULL,
    cooldown FLOAT,
    CHECK (
        (type = 'active' AND cast_time IS NOT NULL AND resource IS NOT NULL AND cooldown IS NOT NULL)
        OR
        (type = 'passive' AND cast_time IS NULL AND resource IS NULL AND cooldown IS NULL )
    )
);

CREATE TABLE profession (
    id UUID PRIMARY KEY,
    name VARCHAR(64) NOT NULL
);

CREATE TABLE guild (
    id UUID PRIMARY KEY,
    name VARCHAR(24) UNIQUE NOT NULL,
    description TEXT,
    type guild_type NOT NULL
);

CREATE TABLE community (
    id UUID PRIMARY KEY,
    name VARCHAR(24) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE quest (
    id UUID PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    description TEXT NOT NULL,
    gold INT DEFAULT 0 NOT NULL CHECK (gold > -1),
    silver INT DEFAULT 0 NOT NULL CHECK (silver > -1),
    copper INT DEFAULT 0 NOT NULL CHECK (copper > -1)
);

CREATE TABLE mount (
    id UUID PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    type mount_type NOT NULL
);

CREATE TABLE pet (
    id UUID PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    pet_type pet_type NOT NULL,
    quality pet_quality NOT NULL
);

CREATE TABLE toy (
    id UUID PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE title (
    id UUID PRIMARY KEY,
    name VARCHAR(64) NOT NULL
);


--  13