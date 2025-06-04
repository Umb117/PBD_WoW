-- Query 1: Character profile
CREATE INDEX idx_game_character_total_exp_gained ON game_character(total_exp_gained);
CREATE INDEX idx_game_character_race_id ON game_character(race_id);
CREATE INDEX idx_game_character_class_id ON game_character(class_id);
CREATE INDEX idx_game_character_spec_id ON game_character(spec_id);
CREATE INDEX idx_game_character_server_id ON game_character(server_id);
CREATE INDEX idx_guild_character_character_id ON guild_character(character_id);
CREATE INDEX idx_guild_character_guild_id ON guild_character(guild_id);
CREATE INDEX idx_character_equipment_character_id ON character_equipment(character_id);
CREATE INDEX idx_character_equipment_item_id ON character_equipment(item_id);
CREATE INDEX idx_character_ability_character_id ON character_ability(character_id);
CREATE INDEX idx_character_ability_ability_id ON character_ability(ability_id);

-- Query 2: Guild statistics
CREATE INDEX idx_guild_character_guild_id ON guild_character(guild_id);
CREATE INDEX idx_game_character_gold ON game_character(gold);

-- Query 3: Quest progress
CREATE INDEX idx_character_quest_character_id_status ON character_quest(character_id, status);
CREATE INDEX idx_character_quest_quest_id ON character_quest(quest_id);
CREATE INDEX idx_character_quest_objectives_character_quest_id ON character_quest_objectives(character_quest_id);
CREATE INDEX idx_character_quest_objectives_objective_id ON character_quest_objectives(objective_id);
CREATE INDEX idx_objective_target_item_id ON objective(target_item_id);
CREATE INDEX idx_objective_target_mob_id ON objective(target_mob_id);

-- Query 4: Auction lots
CREATE INDEX idx_auction_lot_expires_at ON auction_lot(expires_at);
CREATE INDEX idx_auction_lot_item_id ON auction_lot(item_id);
CREATE INDEX idx_auction_lot_character_id ON auction_lot(character_id);
CREATE INDEX idx_item_binding_type_quality ON item(binding_type, quality);
CREATE INDEX idx_auction_lot_gold ON auction_lot(gold);

-- Query 5: Character profession
CREATE INDEX idx_character_profession_character_id ON character_profession(character_id);
CREATE INDEX idx_character_profession_profession_id ON character_profession(profession_id);
CREATE INDEX idx_character_recipe_character_id ON character_recipe(character_id);
CREATE INDEX idx_character_recipe_recipe_id ON character_recipe(recipe_id);
CREATE INDEX idx_character_profession_skill_level ON character_profession(skill_level);

-- Query 6: Character mail
CREATE INDEX idx_writing_recipient_id_expires_at ON writing(recipient_id, expires_at);
CREATE INDEX idx_writing_sender_id ON writing(sender_id);
CREATE INDEX idx_writing_items_writing_id ON writing_items(writing_id);
CREATE INDEX idx_writing_items_item_id ON writing_items(item_id);

-- Query 7: Top mobs by loot
CREATE INDEX idx_mob_location_id ON mob(location_id);
CREATE INDEX idx_mob_loot_mob_id ON mob_loot(mob_id);
CREATE INDEX idx_mob_loot_item_id ON mob_loot(item_id);
CREATE INDEX idx_item_quality ON item(quality);
CREATE INDEX idx_item_gold ON item(gold);

-- Query 8: Account collection
CREATE INDEX idx_game_character_account_id ON game_character(account_id);
CREATE INDEX idx_account_mount_account_id ON account_mount(account_id);
CREATE INDEX idx_account_pet_account_id ON account_pet(account_id);
CREATE INDEX idx_account_toy_account_id ON account_toy(account_id);

-- Query 9: Character abilities
CREATE INDEX idx_specialization_ability_ability_id ON specialization_ability(ability_id);
CREATE INDEX idx_specialization_ability_specialization_id ON specialization_ability(specialization_id);
CREATE INDEX idx_class_ability_ability_id ON class_ability(ability_id);
CREATE INDEX idx_class_ability_class_id ON class_ability(class_id);
CREATE INDEX idx_race_ability_ability_id ON race_ability(ability_id);
CREATE INDEX idx_race_ability_race_id ON race_ability(race_id);

-- Query 10: Character bank and inventory
CREATE INDEX idx_inventory_items_character_id ON inventory_items(character_id);
CREATE INDEX idx_inventory_items_bag_id ON inventory_items(bag_id);
CREATE INDEX idx_inventory_items_item_id ON inventory_items(item_id);
CREATE INDEX idx_bank_character_id ON bank(character_id);
CREATE INDEX idx_bank_item_id ON bank(item_id);
CREATE INDEX idx_item_item_level ON item(item_level);

-- Query 11: Item distribution
CREATE INDEX idx_item_expansion_id ON item(expansion_id);
CREATE INDEX idx_character_equipment_item_id ON character_equipment(item_id);