import os
import datetime

from faker import Faker
from faker.providers import internet, date_time, person, misc
from psycopg2.extras import execute_values

fake = Faker()
fake.add_provider(internet)
fake.add_provider(date_time)
fake.add_provider(person)
fake.add_provider(misc)

SEED_COUNT = int(os.getenv('SEED_COUNT'))

def seed(cur):
    cur.execute("SELECT id FROM expansion")
    expansion_ids = [row[0] for row in cur.fetchall()]
    generate_locations(cur , expansion_ids)
    print("Ok0" , flush=True)

    cur.execute("SELECT id FROM location")
    location_ids = [row[0] for row in cur.fetchall()]
    generate_races(cur , location_ids)
    print("Ok1" , flush=True)

    cur.execute("SELECT id FROM class")
    class_ids = [row[0] for row in cur.fetchall()]
    generate_specializations(cur , class_ids)
    print("Ok2" , flush=True)

    cur.execute("SELECT id FROM account")
    account_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM race")
    race_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM specialization")
    spec_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM server")
    server_ids = [row[0] for row in cur.fetchall()]
    generate_game_characters(cur , account_ids , race_ids , class_ids , spec_ids , server_ids , expansion_ids ,
                             location_ids)
    print("Ok3" , flush=True)

    generate_items(cur , expansion_ids)
    print("Ok4" , flush=True)
    cur.execute("SELECT id FROM item")
    item_ids = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT id FROM item WHERE item_class = 'armor'")
    armor_item_ids = [row[0] for row in cur.fetchall()]
    generate_armor(cur , armor_item_ids)
    print("Ok5" , flush=True)

    cur.execute("SELECT id FROM item WHERE item_class = 'weapon'")
    weapon_item_ids = [row[0] for row in cur.fetchall()]
    generate_weapon(cur , weapon_item_ids)
    print("Ok6" , flush=True)

    cur.execute("SELECT id FROM item WHERE item_class = 'consumable'")
    consumable_item_ids = [row[0] for row in cur.fetchall()]
    generate_consumable(cur , consumable_item_ids)
    print("Ok7" , flush=True)

    cur.execute("SELECT id FROM item WHERE item_class = 'trade_goods'")
    trade_goods_item_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM profession")
    profession_ids = [row[0] for row in cur.fetchall()]

    generate_trade_goods(cur , trade_goods_item_ids, profession_ids)
    print("Ok8" , flush=True)

    cur.execute("SELECT id FROM item WHERE item_class = 'quest_item'")
    quest_item_item_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM quest")
    quest_ids = [row[0] for row in cur.fetchall()]

    generate_quest_item(cur , quest_item_item_ids, quest_ids)
    print("Ok9" , flush=True)

    cur.execute("SELECT id FROM item WHERE item_class = 'container'")
    container_item_ids = [row[0] for row in cur.fetchall()]

    generate_container(cur , container_item_ids)
    print("Ok10" , flush=True)
    generate_recipes(cur , expansion_ids , profession_ids , trade_goods_item_ids)
    print("Ok11" , flush=True)
    generate_mobs(cur , location_ids)
    print("Ok12" , flush=True)

    cur.execute("SELECT id FROM mob")
    mob_ids = [row[0] for row in cur.fetchall()]

    generate_objectives(cur , mob_ids , quest_item_item_ids , quest_ids)
    print("Ok13" , flush=True)
    generate_dungeons(cur , location_ids , expansion_ids)
    print("Ok14" , flush=True)
    generate_raids(cur , location_ids , expansion_ids)
    print("Ok15" , flush=True)
    generate_currencies(cur , expansion_ids)
    print("Ok16" , flush=True)
    generate_reputations(cur , expansion_ids)
    print("Ok17" , flush=True)

    cur.execute("SELECT id FROM game_character")
    character_ids = [row[0] for row in cur.fetchall()]

    generate_writings(cur , character_ids)
    print("Ok18" , flush=True)

    cur.execute("SELECT id FROM item WHERE binding_type != 'BoP'")
    not_bop_item_ids = [row[0] for row in cur.fetchall()]

    generate_auction_lots(cur , character_ids , not_bop_item_ids)
    print("Ok19" , flush=True)

def generate_locations(cur, expansion_ids):
    locations = []
    for _ in range(SEED_COUNT):
        locations.append((
            fake.uuid4(),
            fake.city()[:64],
            fake.random.choice(expansion_ids)
        ))
    cur.executemany("""
        INSERT INTO location (id, name, expansion_id)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING
    """, locations)

def generate_races(cur, location_ids):
    races = []
    race_names = ['Human', 'Orc', 'Night Elf', 'Undead', 'Tauren',
                 'Gnome', 'Troll', 'Blood Elf', 'Draenei', 'Worgen']
    for name in race_names:
        races.append((
            fake.uuid4(),
            name,
            fake.random.choice(location_ids)  # starting_zone_id
        ))
    cur.executemany("""
        INSERT INTO race (id, name, starting_zone_id)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING
    """, races)

def generate_specializations(cur, class_ids):
    specializations = []
    roles = ['tank', 'dps', 'healer']
    spec_names = ['Protection', 'Fury', 'Arcane', 'Holy', 'Shadow',
                 'Restoration', 'Assassination', 'Beast Mastery']
    for name in spec_names:
        specializations.append((
            fake.uuid4(),
            name,
            fake.random.choice(class_ids),
            fake.random.choice(roles)
        ))
    cur.executemany("""
        INSERT INTO specialization (id, name, class_id, role)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, specializations)

def generate_game_characters(cur, account_ids, race_ids, class_ids, spec_ids, server_ids, expansion_ids, location_ids):
    characters = []

    batch_size = 1000
    characters = []
    batch_count = 0

    for i in range(SEED_COUNT):

        characters.append((
            fake.uuid4(),
            fake.random.choice(account_ids),
            str(i),
            fake.random.choice(['male' , 'female']) ,
            str(fake.random.choice(race_ids)) ,
            str(fake.random.choice(class_ids)) ,
            str(fake.random.choice(spec_ids)) ,
            str(fake.random.choice(server_ids)) ,
            str(fake.random.choice(expansion_ids)) ,
            str(fake.random.choice(location_ids)) ,
            fake.random_int(0 , 10000) ,  # gold
            fake.random_int(0 , 100) ,  # silver
            fake.random_int(0 , 100) ,  # copper
            datetime.timedelta(hours=fake.random_int(0 , 1000)) ,  # total_playtime
            fake.random_int(0 , 100000)  # total_exp_gained
        ))

        if len(characters) >= batch_size:
            batch_count += 1
            print(f"Inserting batch {batch_count} ({len(characters)} records)..." , flush=True)
            execute_values(
                cur ,
                """
                INSERT INTO game_character
                (id, account_id, name, gender, race_id, class_id, spec_id,
                 server_id, expansion_id, location_id, gold, silver, copper,
                 total_playtime, total_exp_gained)
                VALUES %s ON CONFLICT (name) DO NOTHING
                """ ,
                characters
            )
            characters = []

    # Вставка оставшихся записей
    if characters:
        batch_count += 1
        print(f"Inserting final batch {batch_count} ({len(characters)} records)..." , flush=True)
        execute_values(
            cur ,
            """
            INSERT INTO game_character
            (id, account_id, name, gender, race_id, class_id, spec_id,
             server_id, expansion_id, location_id, gold, silver, copper,
             total_playtime, total_exp_gained)
            VALUES %s ON CONFLICT (name) DO NOTHING
            """ ,
            characters
        )

def generate_items(cur, expansion_ids):
    items = []
    for item_class in ['armor', 'weapon', 'consumable', 'trade_goods', 'quest_item', 'container']:
        for _ in range(SEED_COUNT):
            items.append((
                fake.uuid4(),
                fake.unique.catch_phrase()[:255],
                fake.random_int(1, 100),
                fake.random.choice(['common', 'uncommon', 'rare', 'epic', 'legendary', 'artifact']),
                fake.random_int(1, 100),
                fake.random_int(0, 1000),
                fake.random_int(0, 100),
                fake.random_int(0, 100),
                fake.sentence(),
                fake.random.choice(expansion_ids),
                item_class,
                fake.random.choice(['BoP', 'BoE', 'BtA']),
                fake.random_int(0, 110)
        ))
    cur.executemany("""
        INSERT INTO item 
        (id, name, item_level, quality, max_stack, gold, silver, copper, 
         description, expansion_id, item_class, binding_type, required_level)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, items)

def generate_armor(cur, item_ids):
    armors = []
    slots = [
        'head', 'chest', 'legs', 'hands', 'feet',
        'shoulders', 'wrists', 'waist', 'back'
    ]
    for item_id in item_ids:
        armors.append((
            item_id,
            fake.random_int(50, 200) if fake.boolean(70) else None,  # durability
            fake.random.choice(['Plate', 'Mail', 'Leather', 'Cloth']),  # armor_type
            fake.random_int(100, 1000),  # armor_value
            fake.random.choice(slots)
        ))
    cur.executemany("""
        INSERT INTO armor 
        (id, durability, armor_type, armor_value, slot)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, armors)

def generate_weapon(cur, item_ids):
    weapons = []
    types = ['Sword', 'Axe', 'Mace', 'Dagger', 'Staff', 'Bow']
    for item_id in item_ids:
        weapons.append((
            item_id,
            fake.random_int(50, 200) if fake.boolean(70) else None,  # durability
            fake.random_int(50, 300),  # damage_min
            fake.random_int(300, 600),  # damage_max
            round(fake.random.uniform(1.0, 3.5), 1),  # attack_speed
            fake.random.choice(types),  # weapon_type
            fake.random.choice(['One-Handed', 'Two-Handed'])
        ))
    cur.executemany("""
        INSERT INTO weapon 
        (id, durability, damage_min, damage_max, attack_speed, weapon_type, handedness)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, weapons)

def generate_consumable(cur, item_ids):
    consumables = []
    effects = ['Healing', 'Mana', 'Speed Boost', 'Invisibility', 'Damage Buff']
    for item_id in item_ids:
        consumables.append((
            item_id,
            fake.random.choice(effects),
            fake.random_int(10, 3600),  # duration (секунды)
            fake.random_int(60, 1800),  # cooldown
            fake.random_int(1, 5),  # charges
            fake.random_int(0, 60)  # required_level
        ))
    cur.executemany("""
        INSERT INTO consumable 
        (id, effect, duration, cooldown, charges, required_level)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, consumables)

def generate_trade_goods(cur, item_ids, profession_ids):
    trade_goods = []
    for item_id in item_ids:
        trade_goods.append((
            item_id,
            fake.random.choice(profession_ids)
        ))
    cur.executemany("""
        INSERT INTO trade_goods 
        (id, profession_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """, trade_goods)

def generate_quest_item(cur, item_ids, quest_ids):
    quest_items = []
    for item_id in item_ids:
        quest_items.append((
            item_id,
            fake.random.choice(quest_ids),
            fake.boolean()  # is_quest_start
        ))
    cur.executemany("""
        INSERT INTO quest_item 
        (id, quest_id, is_quest_start)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING
    """, quest_items)

def generate_container(cur, item_ids):
    containers = []
    for item_id in item_ids:
        containers.append((
            item_id,
            fake.random_int(4, 20)  # container_size
        ))
    cur.executemany("""
        INSERT INTO container 
        (id, container_size)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """, containers)

def generate_recipes(cur, expansion_ids, profession_ids, item_ids):
    recipes = []
    for _ in range(SEED_COUNT):
        recipes.append((
            fake.uuid4(),
            fake.unique.catch_phrase()[:128],
            fake.random.choice(expansion_ids),
            fake.random.choice(profession_ids),
            fake.random.choice(item_ids),
            fake.random_int(0, 300)  # required_skill
        ))
    cur.executemany("""
        INSERT INTO recipe 
        (id, name, expansion_id, profession_id, result_item_id, required_skill)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, recipes)

def generate_mobs(cur, location_ids):
    mobs = []
    for _ in range(SEED_COUNT):
        mobs.append((
            fake.uuid4(),
            fake.unique.catch_phrase()[:64],
            fake.random.choice(location_ids),
            fake.boolean(),  # is_boss
            fake.random_int(1, 120)
        ))
    cur.executemany("""
        INSERT INTO mob 
        (id, name, location_id, is_boss, level_mob)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, mobs)

def generate_objectives(cur , mob_ids , item_ids , quest_ids):
    objectives = []
    types = ['kill' , 'collect' , 'use']
    for _ in range(SEED_COUNT):
        obj_type = fake.random.choice(types)
        target_mob = fake.random.choice(mob_ids) if obj_type == 'kill' else None
        target_item = fake.random.choice(item_ids) if obj_type == 'collect' else None

        objectives.append((
            fake.uuid4(),
            obj_type ,
            target_mob ,
            target_item ,
            fake.random_int(1 , 20) ,  # quantity
            fake.random.choice(quest_ids)
        ))
    cur.executemany("""
                    INSERT INTO objective
                        (id, type, target_mob_id, target_item_id, quantity, quest_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """ , objectives)

def generate_dungeons(cur, location_ids, expansion_ids):
    dungeons = []
    for _ in range(SEED_COUNT):
        dungeons.append((
            fake.uuid4(),
            fake.unique.catch_phrase()[:64],
            fake.random.choice(location_ids),
            fake.random.choice(expansion_ids)
        ))
    cur.executemany("""
        INSERT INTO dungeon 
        (id, name, location_id, expansion_id)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, dungeons)

def generate_raids(cur, location_ids, expansion_ids):
    raids = []
    for _ in range(SEED_COUNT):
        raids.append((
            fake.uuid4(),
            fake.unique.catch_phrase()[:64],
            fake.random.choice(location_ids),
            fake.random.choice(expansion_ids)
        ))
    cur.executemany("""
        INSERT INTO raid 
        (id, name, location_id, expansion_id)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, raids)

def generate_currencies(cur, expansion_ids):
    currencies = []
    for _ in range(SEED_COUNT):
        currencies.append((
            fake.uuid4(),
            fake.unique.catch_phrase()[:64],
            fake.random.choice(expansion_ids)
        ))
    cur.executemany("""
        INSERT INTO currency 
        (id, name, expansion_id)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING
    """, currencies)

def generate_reputations(cur, expansion_ids):
    reputations = []
    for _ in range(SEED_COUNT):
        reputations.append((
            fake.uuid4(),
            fake.unique.company()[:64],
            fake.random.choice(expansion_ids)
        ))
    cur.executemany("""
        INSERT INTO reputation 
        (id, name, expansion_id)
        VALUES (%s, %s, %s)
        ON CONFLICT (name) DO NOTHING
    """, reputations)

def generate_writings(cur, character_ids):
    writings = []
    for _ in range(int(SEED_COUNT/2)):
        # sender и recipient должны быть разными персонажами
        sender, recipient = fake.random_elements(
            elements=character_ids,
            length=2,
            unique=True
        )
        writings.append((
            fake.uuid4(),
            sender,
            recipient,
            fake.sentence(nb_words=3)[:40],  # subject
            fake.text(max_nb_chars=500),  # body
            fake.random_int(0, 1000),  # gold
            fake.random_int(0, 100),  # silver
            fake.random_int(0, 100),  # copper
            fake.boolean(),  # cod
            datetime.datetime.now() + datetime.timedelta(days=7)  # expires_at
        ))
    cur.executemany("""
        INSERT INTO writing 
        (id, sender_id, recipient_id, subject, body, gold, silver, copper, cod, expires_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, writings)

def generate_auction_lots(cur, character_ids, item_ids):
    auction_lots = []
    for _ in range(SEED_COUNT):
        auction_lots.append((
            fake.uuid4(),
            fake.random.choice(character_ids),
            fake.random.choice(item_ids),
            fake.random_int(1, 20),  # quantity
            fake.random_int(10, 5000),  # gold
            fake.random_int(0, 100),  # silver
            fake.random_int(0, 100),  # copper
            fake.boolean(),  # buyout_mode
            datetime.datetime.now() + datetime.timedelta(days=3)  # expires_at
        ))
    cur.executemany("""
        INSERT INTO auction_lot 
        (id, character_id, item_id, quantity, gold, silver, copper, buyout_mode, expires_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, auction_lots)

if __name__ == "__main__":
    seed()
    print("Сидирование V2 завершено!")