CREATE TABLE login_history (
  account_id UUID NOT NULL REFERENCES account(id),
  ip_address VARCHAR(45) NOT NULL,
  login_time TIMESTAMP NOT NULL,
  device_info jsonb NOT NULL
);

CREATE TABLE account_history (
  account_id UUID NOT NULL REFERENCES account(id),
  changed_field VARCHAR(64) NOT NULL,
  old_value TEXT NOT NULL,
  new_value TEXT NOT NULL,
  changed_at TIMESTAMP NOT NULL
);

CREATE TABLE account_friend (
  account_id UUID NOT NULL REFERENCES account(id),
  friend_id UUID NOT NULL REFERENCES account(id),
  since TIMESTAMP NOT NULL,
  note VARCHAR(128)
);

CREATE TABLE account_ignore (
  account_id UUID NOT NULL REFERENCES account(id),
  ignored_id UUID NOT NULL REFERENCES account(id),
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE community_account (
  account_id UUID NOT NULL REFERENCES account(id),
  community_id UUID NOT NULL REFERENCES community(id)
);

CREATE TABLE account_mount (
  account_id UUID NOT NULL REFERENCES account(id),
  mount_id UUID NOT NULL REFERENCES mount(id)
);

CREATE TABLE account_pet (
  account_id UUID NOT NULL REFERENCES account(id),
  pet_id UUID NOT NULL REFERENCES pet(id)
);

CREATE TABLE account_toy (
  account_id UUID NOT NULL REFERENCES account(id),
  toy_id UUID NOT NULL REFERENCES toy(id)
);

CREATE TABLE account_title (
  account_id UUID NOT NULL REFERENCES account(id),
  title_id UUID NOT NULL REFERENCES title(id)
);

CREATE TABLE character_equipment (
  character_id UUID NOT NULL REFERENCES game_character(id),
  slot_type equipment_slot NOT NULL,
  item_id UUID NOT NULL REFERENCES item(id)
);

CREATE TABLE bags (
    id UUID PRIMARY KEY,
    character_id UUID NOT NULL REFERENCES game_character(id),
    slot INT NOT NULL CHECK (slot BETWEEN 0 AND 4), -- 0-4 (5 слотов)
    item_id UUID NOT NULL REFERENCES item(id),
    size INT NOT NULL CHECK (size > 0)
);

CREATE TABLE inventory_items (
  id UUID PRIMARY KEY,
  character_id UUID NOT NULL REFERENCES game_character(id),
  bag_id UUID NOT NULL REFERENCES bags(id),
  position_in_bag INT NOT NULL CHECK (position_in_bag > -1),
  item_id UUID NOT NULL REFERENCES item(id),
  quantity INT NOT NULL DEFAULT 1 CHECK (quantity > 0)
);

CREATE TABLE bank (
  character_id UUID NOT NULL REFERENCES game_character(id),
  item_id UUID NOT NULL REFERENCES item(id),
  slot INT NOT NULL CHECK (slot >= 0),
  quantity INT NOT NULL DEFAULT 1 CHECK (quantity >= 0)
);

CREATE TABLE writing_items (
  writing_id UUID NOT NULL REFERENCES writing(id),
  item_id UUID NOT NULL REFERENCES item(id)
);

CREATE TABLE character_currency (
  character_id UUID NOT NULL REFERENCES game_character(id),
  currency_id UUID NOT NULL REFERENCES currency(id),
  amount INT NOT NULL CHECK (amount > 0)
);

CREATE TABLE character_reputation (
  character_id UUID NOT NULL REFERENCES game_character(id),
  faction_id UUID NOT NULL REFERENCES reputation(id),
  char_level character_reputation_level NOT NULL,
  value INT NOT NULL CHECK (value > 0)
);

CREATE TABLE guild_character (
  character_id UUID NOT NULL REFERENCES game_character(id),
  guild_id UUID NOT NULL REFERENCES guild(id),
  player_rank player_rank_type NOT NULL
);

CREATE TABLE race_ability (
  ability_id UUID NOT NULL REFERENCES ability(id),
  race_id UUID NOT NULL REFERENCES race(id)
);

CREATE TABLE class_ability (
  ability_id UUID NOT NULL REFERENCES ability(id),
  class_id UUID NOT NULL REFERENCES class(id)
);

CREATE TABLE specialization_ability (
  ability_id UUID NOT NULL REFERENCES ability(id),
  specialization_id UUID NOT NULL REFERENCES specialization(id)
);

CREATE TABLE mob_ability (
  ability_id UUID NOT NULL REFERENCES ability(id),
  mob_id UUID NOT NULL REFERENCES mob(id)
);

CREATE TABLE character_ability (
  character_id UUID NOT NULL REFERENCES game_character(id),
  ability_id UUID NOT NULL REFERENCES ability(id)
);

CREATE TABLE recipe_ingredients (
  recipe_id UUID NOT NULL REFERENCES recipe(id),
  item_id UUID NOT NULL REFERENCES item(id),
  quantity INT NOT NULL CHECK (quantity > 0)
);

CREATE TABLE character_recipe (
  character_id UUID NOT NULL REFERENCES game_character(id),
  recipe_id UUID NOT NULL REFERENCES recipe(id)
);

CREATE TABLE character_profession (
  character_id UUID NOT NULL REFERENCES game_character(id),
  profession_id UUID NOT NULL REFERENCES profession(id),
  skill_level INT NOT NULL DEFAULT 0 CHECK (skill_level > -1)
);

CREATE TABLE quest_rewards (
  quest_id UUID NOT NULL REFERENCES quest(id),
  item_id UUID NOT NULL REFERENCES item(id)
);

CREATE TABLE character_quest (
  id UUID PRIMARY KEY,
  character_id UUID NOT NULL REFERENCES game_character(id),
  quest_id UUID NOT NULL REFERENCES quest(id),
  status character_quest_status NOT NULL
);

CREATE TABLE character_quest_objectives (
  objective_id UUID NOT NULL REFERENCES objective(id),
  character_quest_id UUID NOT NULL REFERENCES character_quest(id),
  current INT NOT NULL CHECK (current > 0)
);

CREATE TABLE mob_loot (
  mob_id UUID NOT NULL REFERENCES mob(id),
  item_id UUID NOT NULL REFERENCES item(id),
  chance FLOAT NOT NULL CHECK (chance > 0)
);

CREATE TABLE class_race (
  class_id UUID NOT NULL REFERENCES class(id),
  race_id UUID NOT NULL REFERENCES race(id)
);

CREATE TABLE item_stats (
  item_id UUID NOT NULL REFERENCES item(id),
  stat_type item_state_type NOT NULL,
  value INT NOT NULL CHECK (value > 0)
);

-- 31