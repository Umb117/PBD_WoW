import json
import os

from faker import Faker
from faker.providers import internet, date_time, person, misc

fake = Faker()
fake.add_provider(internet)
fake.add_provider(date_time)
fake.add_provider(person)
fake.add_provider(misc)

SEED_COUNT = int(os.getenv('SEED_COUNT'))

def seed(cur):
    cur.execute("SELECT id FROM account")
    account_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM community")
    community_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM mount")
    mount_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM pet")
    pet_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM toy")
    toy_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM title")
    title_ids = [row[0] for row in cur.fetchall()]

    generate_login_history(cur, account_ids)
    print("Ok0" , flush=True)
    generate_account_history(cur , account_ids)
    print("Ok1" , flush=True)
    generate_account_friend(cur , account_ids)
    print("Ok2" , flush=True)
    generate_account_ignore(cur , account_ids)
    print("Ok3" , flush=True)
    generate_community_account(cur , account_ids , community_ids)
    print("Ok4" , flush=True)
    generate_account_mount(cur , account_ids , mount_ids)
    print("Ok5" , flush=True)
    generate_account_pet(cur , account_ids , pet_ids)
    print("Ok6" , flush=True)
    generate_account_toy(cur , account_ids , toy_ids)
    print("Ok7" , flush=True)
    generate_account_title(cur , account_ids , title_ids)
    print("Ok8" , flush=True)

    cur.execute("SELECT id FROM item WHERE item_class IN ('armor', 'weapon')")
    armor_weapon_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM writing")
    writing_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM currency")
    currency_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM reputation")
    faction_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM guild")
    guild_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM game_character")
    character_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM item WHERE item_class = 'container'")
    container_item_ids = [row[0] for row in cur.fetchall()]

    slot_types = ['head', 'neck', 'shoulders', 'chest', 'back', 'wrists',
    'hands', 'waist', 'legs', 'feet', 'finger_1', 'finger_2',
    'trinket_1', 'trinket_2', 'main_hand', 'off_hand', 'tabard', 'shirt']
    generate_character_equipment(cur , character_ids , armor_weapon_ids , slot_types)
    print("Ok9" , flush=True)
    generate_bags(cur, character_ids, container_item_ids)
    print("Ok10" , flush=True)

    cur.execute("SELECT id FROM bags")
    bag_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM item")
    item_ids = [row[0] for row in cur.fetchall()]

    generate_inventory_items(cur, character_ids, bag_ids, item_ids)
    print("Ok11" , flush=True)
    generate_bank(cur, character_ids, item_ids)
    print("Ok12" , flush=True)
    generate_writing_items(cur, writing_ids, item_ids)
    print("Ok13" , flush=True)
    generate_character_currency(cur, character_ids, currency_ids)
    print("Ok14" , flush=True)
    generate_character_reputation(cur, character_ids, faction_ids)
    print("Ok15" , flush=True)
    generate_guild_character(cur, character_ids, guild_ids)
    print("Ok16" , flush=True)

    cur.execute("SELECT id FROM ability")
    ability_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM race")
    race_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM class")
    class_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM specialization")
    spec_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM mob")
    mob_ids = [row[0] for row in cur.fetchall()]

    generate_race_ability(cur , race_ids , ability_ids)
    print("Ok17" , flush=True)
    generate_class_ability(cur , class_ids , ability_ids)
    print("Ok18" , flush=True)
    generate_specialization_ability(cur , spec_ids , ability_ids)
    print("Ok19" , flush=True)
    generate_mob_ability(cur , mob_ids , ability_ids)
    print("Ok20" , flush=True)
    generate_character_ability(cur , character_ids , ability_ids)
    print("Ok21" , flush=True)

    cur.execute("SELECT id FROM recipe")
    recipe_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM item WHERE item_class = 'trade_goods'")
    trade_goods_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM profession")
    profession_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM quest")
    quest_ids = [row[0] for row in cur.fetchall()]

    generate_recipe_ingredients(cur , recipe_ids , trade_goods_ids)
    print("Ok22" , flush=True)
    generate_character_recipe(cur , character_ids , recipe_ids)
    print("Ok23" , flush=True)
    generate_character_profession(cur , character_ids , profession_ids)
    print("Ok24" , flush=True)
    generate_quest_rewards(cur , quest_ids , item_ids)
    print("Ok25" , flush=True)
    generate_character_quest(cur , character_ids , quest_ids)
    print("Ok26" , flush=True)

    cur.execute("SELECT id FROM objective")
    objective_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM character_quest")
    character_quest_ids = [row[0] for row in cur.fetchall()]

    generate_character_quest_objectives(cur , objective_ids , character_quest_ids)
    print("Ok27" , flush=True)
    generate_mob_loot(cur , mob_ids , item_ids)
    print("Ok28" , flush=True)
    generate_class_race(cur , class_ids , race_ids)
    print("Ok29" , flush=True)
    generate_item_stats(cur , item_ids)
    print("Ok30" , flush=True)


def generate_login_history(cur , account_ids):
    logins = []
    for _ in range(SEED_COUNT):
        logins.append((
            fake.random.choice(account_ids) ,
            fake.ipv4() ,  # ip_address
            fake.date_time_this_year() ,  # login_time
            json.dumps({  # device_info
                "os": fake.random.choice(["Windows" , "macOS" , "Linux" , "iOS" , "Android"]) ,
                "browser": fake.chrome() ,
                "device": fake.user_agent()
            })
        ))
    cur.executemany("""
                    INSERT INTO login_history
                        (account_id, ip_address, login_time, device_info)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """ , logins)

def generate_account_history(cur , account_ids):
    history = []
    fields = ['email' , 'password' , 'phone' , 'subscription_status']
    for account_id in account_ids:
        for _ in range(fake.random_int(0 , 3)):  # 0-3 изменений на аккаунт
            field = fake.random.choice(fields)
            old_val = fake.email() if field == 'email' else fake.password() if field == 'password' else fake.phone_number() if field == 'phone' else 'active'
            new_val = fake.email() if field == 'email' else fake.password() if field == 'password' else fake.phone_number() if field == 'phone' else 'inactive'

            history.append((
                account_id ,
                field ,
                old_val ,
                new_val ,
                fake.date_time_this_year()
            ))
    cur.executemany("""
                    INSERT INTO account_history
                        (account_id, changed_field, old_value, new_value, changed_at)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """ , history)

def generate_account_friend(cur , account_ids):
    friends = []
    added_pairs = set()  # Для отслеживания уникальных пар

    for _ in range(SEED_COUNT * 2):
        acc_id = fake.random.choice(account_ids)
        friend_id = fake.random.choice([id for id in account_ids if id != acc_id])

        # Проверяем, что пара не добавлена в любом порядке
        if (acc_id , friend_id) not in added_pairs and (friend_id , acc_id) not in added_pairs:
            added_pairs.add((acc_id , friend_id))
            friends.append((
                acc_id ,
                friend_id ,
                fake.date_time_this_decade() ,
                fake.sentence()[:128] if fake.boolean(40) else None
            ))

    cur.executemany("""
                    INSERT INTO account_friend
                        (account_id, friend_id, since, note)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """ , friends)

def generate_account_ignore(cur , account_ids):
    ignores = []
    added_pairs = set()  # Для уникальности

    for _ in range(SEED_COUNT):
        acc_id = fake.random.choice(account_ids)
        ignored_id = fake.random.choice([id for id in account_ids if id != acc_id])

        if (acc_id , ignored_id) not in added_pairs:
            added_pairs.add((acc_id , ignored_id))
            ignores.append((
                acc_id ,
                ignored_id ,
                fake.date_time_this_year()
            ))

    cur.executemany("""
                    INSERT INTO account_ignore
                        (account_id, ignored_id, created_at)
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """ , ignores)

def generate_community_account(cur , account_ids , community_ids):
    links = []
    added_pairs = set()

    for _ in range(SEED_COUNT * 3):
        acc_id = fake.random.choice(account_ids)
        comm_id = fake.random.choice(community_ids)

        if (acc_id , comm_id) not in added_pairs:
            added_pairs.add((acc_id , comm_id))
            links.append((acc_id , comm_id))

    cur.executemany("""
                    INSERT INTO community_account
                        (account_id, community_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                    """ , links)

def generate_account_mount(cur , account_ids , mount_ids):
    mounts = set()
    for _ in range(SEED_COUNT):
        mounts.add((
            fake.random.choice(account_ids) ,
            fake.random.choice(mount_ids)
        ))
    cur.executemany("""
                    INSERT INTO account_mount
                        (account_id, mount_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                    """ , list(mounts))

def generate_account_pet(cur , account_ids , pet_ids):
    pets = set()
    for _ in range(SEED_COUNT):
        pets.add((
            fake.random.choice(account_ids) ,
            fake.random.choice(pet_ids)
        ))
    cur.executemany("""
                    INSERT INTO account_pet
                        (account_id, pet_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                    """ , list(pets))

def generate_account_toy(cur , account_ids , toy_ids):
    toys = set()
    for _ in range(SEED_COUNT):
        toys.add((
            fake.random.choice(account_ids) ,
            fake.random.choice(toy_ids)
        ))
    cur.executemany("""
                    INSERT INTO account_toy
                        (account_id, toy_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                    """ , list(toys))

def generate_account_title(cur , account_ids , title_ids):
    titles = set()
    for _ in range(SEED_COUNT):
        titles.add((
            fake.random.choice(account_ids) ,
            fake.random.choice(title_ids)
        ))
    cur.executemany("""
                    INSERT INTO account_title
                        (account_id, title_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                    """ , list(titles))

def generate_character_equipment(cur, character_ids, item_ids, slot_types):
    equipment = []
    for _ in range(SEED_COUNT):
        char_id = fake.random.choice(character_ids)
        slot = fake.random.choice(slot_types)

        item_id = fake.random.choice(item_ids)
        equipment.append((
            char_id,
            slot,
            item_id
        ))
    cur.executemany("""
        INSERT INTO character_equipment 
        (character_id, slot_type, item_id)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING
    """, equipment)

def generate_bags(cur, character_ids, container_item_ids):
    bags = []
    for char_id in character_ids:
        for slot in range(5):  # 0-4 слотов
            bags.append((
                fake.uuid4(),
                char_id,
                slot,
                fake.random.choice(container_item_ids),
                fake.random_int(4, 20)  # size
            ))
    cur.executemany("""
        INSERT INTO bags 
        (id, character_id, slot, item_id, size)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, bags)

def generate_inventory_items(cur, character_ids, bag_ids, item_ids):
    inventory = []
    for _ in range(SEED_COUNT * 10):
        char_id = fake.random.choice(character_ids)
        bag_id = fake.random.choice(bag_ids)
        position = fake.random_int(0, 20)  # зависит от размера сумки
        inventory.append((
            fake.uuid4(),
            char_id,
            bag_id,
            position,
            fake.random.choice(item_ids),
            fake.random_int(1, 100)  # quantity
        ))
    cur.executemany("""
        INSERT INTO inventory_items 
        (id, character_id, bag_id, position_in_bag, item_id, quantity)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, inventory)

def generate_bank(cur, character_ids, item_ids):
    bank = []
    for _ in range(SEED_COUNT * 5):
        bank.append((
            fake.random.choice(character_ids),
            fake.random.choice(item_ids),
            fake.random_int(0, 100),  # slot
            fake.random_int(1, 200)  # quantity
        ))
    cur.executemany("""
        INSERT INTO bank 
        (character_id, item_id, slot, quantity)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, bank)

def generate_writing_items(cur, writing_ids, item_ids):
    writings = []
    for _ in range(SEED_COUNT):
        writings.append((
            fake.random.choice(writing_ids),
            fake.random.choice(item_ids)
        ))
    cur.executemany("""
        INSERT INTO writing_items 
        (writing_id, item_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """, writings)

def generate_character_currency(cur, character_ids, currency_ids):
    currencies = []
    for _ in range(SEED_COUNT):
        currencies.append((
            fake.random.choice(character_ids),
            fake.random.choice(currency_ids),
            fake.random_int(1, 10000)  # amount
        ))
    cur.executemany("""
        INSERT INTO character_currency 
        (character_id, currency_id, amount)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING
    """, currencies)

def generate_character_reputation(cur, character_ids, faction_ids):
    reputations = []
    levels = ['hated', 'hostile', 'unfriendly', 'neutral',
            'friendly', 'honored', 'revered', 'exalted']
    for _ in range(SEED_COUNT):
        reputations.append((
            fake.random.choice(character_ids),
            fake.random.choice(faction_ids),
            fake.random.choice(levels),
            fake.random_int(1, 9999)  # value
        ))
    cur.executemany("""
        INSERT INTO character_reputation 
        (character_id, faction_id, char_level, value)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, reputations)

def generate_guild_character(cur, character_ids, guild_ids):
    guild_links = []
    ranks = ['recruit', 'participant', 'veteran', 'officer', 'guild master']
    for char_id in character_ids:
        guild_links.append((
            char_id,
            fake.random.choice(guild_ids),
            fake.random.choice(ranks)
        ))
    cur.executemany("""
        INSERT INTO guild_character 
        (character_id, guild_id, player_rank)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING
    """, guild_links)

def generate_race_ability(cur , race_ids , ability_ids):
    data = set()
    for _ in range(SEED_COUNT):
        race_id = fake.random.choice(race_ids)
        ability_id = fake.random.choice(ability_ids)
        data.add((race_id , ability_id))

    cur.executemany("""
                    INSERT INTO race_ability (race_id, ability_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                    """ , list(data))

def generate_class_ability(cur , class_ids , ability_ids):
    data = set()
    for _ in range(SEED_COUNT):
        class_id = fake.random.choice(class_ids)
        ability_id = fake.random.choice(ability_ids)
        data.add((class_id , ability_id))

    cur.executemany("""
                    INSERT INTO class_ability (class_id, ability_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                    """ , list(data))

def generate_specialization_ability(cur , specialization_ids , ability_ids):
    data = set()
    for _ in range(SEED_COUNT):
        spec_id = fake.random.choice(specialization_ids)
        ability_id = fake.random.choice(ability_ids)
        data.add((spec_id , ability_id))

    cur.executemany("""
                    INSERT INTO specialization_ability (specialization_id, ability_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                    """ , list(data))

def generate_mob_ability(cur , mob_ids , ability_ids):
    data = set()
    for _ in range(SEED_COUNT):
        mob_id = fake.random.choice(mob_ids)
        ability_id = fake.random.choice(ability_ids)
        data.add((mob_id , ability_id))

    cur.executemany("""
                    INSERT INTO mob_ability (mob_id, ability_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                    """ , list(data))

def generate_character_ability(cur , character_ids , ability_ids):
    data = set()
    for _ in range(SEED_COUNT):
        char_id = fake.random.choice(character_ids)
        ability_id = fake.random.choice(ability_ids)
        data.add((char_id , ability_id))

    cur.executemany("""
                    INSERT INTO character_ability (character_id, ability_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                    """ , list(data))

def generate_recipe_ingredients(cur , recipe_ids , item_ids):
    ingredients = []
    for recipe_id in recipe_ids:
        ing_num = fake.random_int(1, 3)
        for _ in range(ing_num):
            ingredients.append((
                recipe_id ,
                fake.random.choice(item_ids) ,
                fake.random_int(1 , 10)  # quantity
            ))

    cur.executemany("""
                    INSERT INTO recipe_ingredients (recipe_id, item_id, quantity)
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """ , ingredients)

def generate_character_recipe(cur , character_ids , recipe_ids):
    data = set()
    for _ in range(SEED_COUNT):
        data.add((
            fake.random.choice(character_ids) ,
            fake.random.choice(recipe_ids)
        ))

    cur.executemany("""
                    INSERT INTO character_recipe (character_id, recipe_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                    """ , list(data))

def generate_character_profession(cur, character_ids, profession_ids):
    data = set()
    for _ in range(SEED_COUNT):
        char_id = fake.random.choice(character_ids)
        profession_id = fake.random.choice(profession_ids)
        data.add((
            char_id,
            profession_id,
            fake.random_int(0, 300)  # skill_level
        ))
    cur.executemany("""
        INSERT INTO character_profession 
        (character_id, profession_id, skill_level)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING
    """, list(data))

def generate_quest_rewards(cur, quest_ids, item_ids):
    rewards = []
    for quest_id in quest_ids:
        rewards.append((
            quest_id,
            fake.random.choice(item_ids)
        ))
    cur.executemany("""
        INSERT INTO quest_rewards 
        (quest_id, item_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """, rewards)

def generate_character_quest(cur, character_ids, quest_ids):
    quests = []
    statuses = ['active', 'completed', 'failed']
    for _ in range(SEED_COUNT):
        quests.append((
            fake.uuid4(),
            fake.random.choice(character_ids),
            fake.random.choice(quest_ids),
            fake.random.choice(statuses)
        ))
    cur.executemany("""
        INSERT INTO character_quest 
        (id, character_id, quest_id, status)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, quests)

def generate_character_quest_objectives(cur, objective_ids, character_quest_ids):
    objectives = []
    for cq_id in character_quest_ids:
        # 1-3 цели на квест
        for _ in range(fake.random_int(1, 3)):
            objectives.append((
                fake.random.choice(objective_ids),
                cq_id,
                fake.random_int(1, 20)  # current
            ))
    cur.executemany("""
        INSERT INTO character_quest_objectives 
        (objective_id, character_quest_id, current)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING
    """, objectives)

def generate_mob_loot(cur, mob_ids, item_ids):
    loot = []
    for mob_id in mob_ids:
        # 1-5 предметов на моба
        for _ in range(fake.random_int(1, 5)):
            loot.append((
                mob_id,
                fake.random.choice(item_ids),
                round(fake.random.uniform(0.1, 0.5), 1)  # chance (10%-50%)
            ))
    cur.executemany("""
        INSERT INTO mob_loot 
        (mob_id, item_id, chance)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING
    """, loot)

def generate_class_race(cur, class_ids, race_ids):
    data = set()
    for _ in range(SEED_COUNT):
        data.add((
            fake.random.choice(class_ids),
            fake.random.choice(race_ids)
        ))
    cur.executemany("""
        INSERT INTO class_race 
        (class_id, race_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """, list(data))

def generate_item_stats(cur, item_ids):
    stats = []
    stat_types = ['Intellect', 'Agility', 'Strength', 'Stamina', 'Armor', 'Critical Strike Chance',
 'Haste', 'Mastery', 'Versatility', 'Speed', 'Leech', 'Avoidance']
    for item_id in item_ids:
        # 1-3 стата на предмет
        for _ in range(fake.random_int(1, 3)):
            stats.append((
                item_id,
                fake.random.choice(stat_types),
                fake.random_int(1, 100)
            ))
    cur.executemany("""
        INSERT INTO item_stats 
        (item_id, stat_type, value)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING
    """, stats)

if __name__ == "__main__":
    seed()
    print("Сидирование V3 завершено!")