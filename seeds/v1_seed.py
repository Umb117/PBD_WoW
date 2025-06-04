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
    generate_accounts(cur)
    print("Ok0", flush=True)
    generate_servers(cur)
    print("Ok1", flush=True)
    generate_expansions(cur)
    print("Ok2", flush=True)
    generate_classes(cur)
    print("Ok3", flush=True)
    generate_abilities(cur)
    print("Ok4", flush=True)
    generate_professions(cur)
    print("Ok5", flush=True)
    generate_guilds(cur)
    print("Ok6", flush=True)
    generate_communities(cur)
    print("Ok7", flush=True)
    generate_quests(cur)
    print("Ok8", flush=True)
    generate_mounts(cur)
    print("Ok9", flush=True)
    generate_pets(cur)
    print("Ok10", flush=True)
    generate_toys(cur)
    print("Ok11", flush=True)
    generate_titles(cur)
    print("Ok12", flush=True)

def generate_accounts(cur):
    accounts = []
    for _ in range(SEED_COUNT):
        accounts.append((
            fake.uuid4(),
            fake.unique.user_name()[:12],
            fake.sha256(),
            fake.unique.email(),
            fake.unique.phone_number()[:20],
            fake.first_name(),
            fake.last_name(),
            fake.date_of_birth(),
            fake.country_code(),
            'inactive',
            None
        ))
    cur.executemany("""
        INSERT INTO account 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, accounts)

def generate_servers(cur):
    servers = []
    regions = ['EU', 'US', 'ASIA']
    for _ in range(SEED_COUNT):
        servers.append((
            fake.uuid4(),
            fake.unique.company()[:64],
            fake.random.choice(regions)
        ))
    cur.executemany("""
                    INSERT INTO server
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """ , servers)

def generate_expansions(cur):
    expansions = []
    levels_tens = [1, 40, 50, 60, 70, 80, 90, 100]
    for _ in range(SEED_COUNT):
        min_level = fake.random.choice(levels_tens)
        if min_level == 1:
            max_level = 40
        else:
            max_level = min_level + 10
        expansions.append((
            fake.uuid4(),
            fake.unique.company()[:100],
            min_level,
            max_level
        ))
    cur.executemany("""
                    INSERT INTO expansion
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """, expansions)

def generate_classes(cur):
    classes = []
    class_names = ['Warrior' , 'Mage' , 'Rogue' , 'Priest' , 'Druid',
                   'Monk', 'Warlock', 'Death Knight', 'Demon Hunter',
                   'Paladin', 'Hunter', 'Shaman']
    for name in class_names:
        classes.append((
            fake.uuid4() ,
            name,
            fake.text()[:300]
        ))
    cur.executemany("""
                    INSERT INTO class
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """ , classes)

def generate_abilities(cur):
    abilities = []
    ability_types = ['active' , 'passive']
    resources = ['mana' , 'energy' , 'rage' , 'combo_points']
    for _ in range(SEED_COUNT):
        # Для пассивных способностей убираем cast_time, resource и cooldown
        ab_type = fake.random.choice(ability_types)
        cast_time = fake.pyfloat(min_value=0.5 , max_value=5.0) if ab_type == 'active' else None
        resource = fake.random.choice(resources) if ab_type == 'active' else None
        cooldown = fake.pyfloat(min_value=1.0 , max_value=30.0) if ab_type == 'active' else None

        abilities.append((
            fake.uuid4() ,
            fake.unique.catch_phrase()[:64] ,
            fake.text()[:500] ,
            ab_type ,
            cast_time ,
            resource ,
            fake.pyfloat(min_value=5 , max_value=40) ,  # range
            cooldown
        ))
    cur.executemany("""
                    INSERT INTO ability
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """ , abilities)

def generate_professions(cur):
    professions = []
    profession_names = ['Alchemy' , 'Blacksmithing' , 'Engineering' , 'Tailoring',
                        'Herbalism', 'Mining', 'Skinning', 'Jewelcrafting',
                        'Enchanting', 'Inscription']
    for name in profession_names:
        professions.append((
            fake.uuid4() ,
            name
        ))
    cur.executemany("""
                    INSERT INTO profession
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                    """ , professions)

def generate_guilds(cur):
    guilds = []
    guild_types = ['PvE' , 'PvP' , 'RP' , 'mixed']
    for _ in range(SEED_COUNT):
        guilds.append((
            fake.uuid4() ,
            fake.unique.company()[:24] ,
            fake.text()[:200] ,
            fake.random.choice(guild_types)
        ))
    cur.executemany("""
                    INSERT INTO guild
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """ , guilds)

def generate_communities(cur):
    communities = []
    for _ in range(SEED_COUNT):
        communities.append((
            fake.uuid4() ,
            fake.unique.company()[:24] ,
            fake.text()[:500]
        ))
    cur.executemany("""
                    INSERT INTO community
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """ , communities)

def generate_quests(cur):
    quests = []
    for _ in range(SEED_COUNT):
        quests.append((
            fake.uuid4() ,
            fake.unique.catch_phrase()[:128] ,
            fake.text()[:1000] ,
            fake.random_int(0 , 500) ,  # gold
            fake.random_int(0 , 100) ,  # silver
            fake.random_int(0 , 100)  # copper
        ))
    cur.executemany("""
                    INSERT INTO quest
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """ , quests)

def generate_mounts(cur):
    mounts = []
    mount_types = ['flying' , 'ground' , 'aquatic']
    for _ in range(SEED_COUNT):
        mounts.append((
            fake.uuid4() ,
            fake.unique.catch_phrase()[:64] ,
            fake.random.choice(mount_types)
        ))
    cur.executemany("""
                    INSERT INTO mount
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """ , mounts)

def generate_pets(cur):
    pets = []
    pet_types = ['humanoid' , 'beast' , 'aquatic' , 'magical' , 'mechanical' , 'dragonkin' , 'undead' , 'elemental' ,
                 'flying']
    qualities = ['poor' , 'common' , 'uncommon' , 'rare']
    for _ in range(SEED_COUNT):
        pets.append((
            fake.uuid4() ,
            fake.unique.catch_phrase()[:64] ,
            fake.random.choice(pet_types) ,
            fake.random.choice(qualities)
        ))
    cur.executemany("""
                    INSERT INTO pet
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """ , pets)

def generate_toys(cur):
    toys = []
    for _ in range(SEED_COUNT):
        toys.append((
            fake.uuid4() ,
            fake.unique.catch_phrase()[:64],
            fake.text()[:350]
        ))
    cur.executemany("""
                    INSERT INTO toy
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """ , toys)

def generate_titles(cur):
    titles = []
    for _ in range(SEED_COUNT):
        titles.append((
            fake.uuid4() ,
            fake.unique.catch_phrase()[:64]
        ))
    cur.executemany("""
                    INSERT INTO title
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                    """ , titles)

if __name__ == "__main__":
    seed()
    print("Сидирование V1 завершено!")