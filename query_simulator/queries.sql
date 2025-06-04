-- Query 1: High selectivity - Detailed character profile with equipment and abilities
-- Purpose: Get full profile of a specific character, including equipment, abilities, and guild
WITH selected_character AS (
    SELECT id FROM game_character WHERE total_exp_gained > 500000 LIMIT 1
)
SELECT
    c.id, c.name, c.gender, c.gold, c.total_playtime,
    r.name AS race_name, cl.name AS class_name, s.name AS spec_name,
    sv.name AS server_name, g.name AS guild_name, gc.player_rank,
    ce.slot_type, i.name AS item_name, i.quality, w.damage_min, w.damage_max,
    a.id AS ability_id, a.name AS ability_name, a.type AS ability_type
FROM game_character c
JOIN race r ON c.race_id = r.id
JOIN class cl ON c.class_id = cl.id
JOIN specialization s ON c.spec_id = s.id
JOIN server sv ON c.server_id = sv.id
LEFT JOIN guild_character gc ON c.id = gc.character_id
LEFT JOIN guild g ON gc.guild_id = g.id
LEFT JOIN character_equipment ce ON c.id = ce.character_id
LEFT JOIN item i ON ce.item_id = i.id
LEFT JOIN weapon w ON i.id = w.id
LEFT JOIN character_ability ca ON c.id = ca.character_id
LEFT JOIN ability a ON ca.ability_id = a.id
WHERE c.id = (SELECT id FROM selected_character);

-- Query 2: Low selectivity - Guild statistics with member count and total gold
-- Purpose: Aggregate statistics for all guilds, including member count and total gold
SELECT
    g.name, g.type, sv.name AS server_name,
    COUNT(DISTINCT gc.character_id) AS member_count,
    SUM(c.gold + c.silver / 100.0 + c.copper / 10000.0) AS total_gold
FROM guild g
JOIN guild_character gc ON g.id = gc.guild_id
JOIN game_character c ON gc.character_id = c.id
JOIN server sv ON c.server_id = sv.id
GROUP BY g.id, g.name, g.type, sv.name
HAVING COUNT(DISTINCT gc.character_id) > 5
ORDER BY total_gold DESC;

-- Query 3: High selectivity - Quest progress for a specific character
-- Purpose: Detailed quest progress for a specific character, including objectives
WITH selected_character AS (
    SELECT id FROM game_character WHERE id IN (SELECT character_id FROM character_quest WHERE status = 'active') LIMIT 1
)
SELECT
    c.name, q.name AS quest_name, q.description, cq.status,
    o.type AS objective_type, o.quantity, cqo.current,
    i.name AS target_item, m.name AS target_mob
FROM game_character c
JOIN character_quest cq ON c.id = cq.character_id
JOIN quest q ON cq.quest_id = q.id
JOIN character_quest_objectives cqo ON cq.id = cqo.character_quest_id
JOIN objective o ON cqo.objective_id = o.id
LEFT JOIN item i ON o.target_item_id = i.id
LEFT JOIN mob m ON o.target_mob_id = m.id
WHERE c.id = (SELECT id FROM selected_character) AND cq.status = 'active'
ORDER BY q.name;

-- Query 4: Medium selectivity - Auction lots with item details
-- Purpose: List active auction lots with non-BoP items and seller info
SELECT
    al.id, al.quantity, al.gold, al.silver, al.copper, al.buyout_mode,
    i.name AS item_name, i.quality, i.item_level,
    c.name AS seller_name, sv.name AS server_name
FROM auction_lot al
JOIN item i ON al.item_id = i.id
JOIN game_character c ON al.character_id = c.id
JOIN server sv ON c.server_id = sv.id
WHERE al.expires_at > CURRENT_TIMESTAMP
  AND i.binding_type != 'BoP'
  AND i.quality IN ('rare', 'epic', 'legendary')
ORDER BY al.gold DESC;

-- Query 5: Low selectivity - Character profession and recipe summary
-- Purpose: Summarize professions and recipes known by characters
SELECT
    c.name, p.name AS profession_name, cp.skill_level,
    COUNT(DISTINCT cr.recipe_id) AS recipe_count,
    AVG(r.required_skill) AS avg_recipe_skill
FROM game_character c
JOIN character_profession cp ON c.id = cp.character_id
JOIN profession p ON cp.profession_id = p.id
LEFT JOIN character_recipe cr ON c.id = cr.character_id
LEFT JOIN recipe r ON cr.recipe_id = r.id
GROUP BY c.id, c.name, p.name, cp.skill_level
HAVING COUNT(DISTINCT cr.recipe_id) > 0
ORDER BY cp.skill_level DESC;

-- Query 6: High selectivity - Character mail with attached items
-- Purpose: Retrieve mail for a specific character with attached items
WITH selected_character AS (
    SELECT id FROM game_character WHERE id IN (
        SELECT recipient_id FROM writing WHERE expires_at > CURRENT_TIMESTAMP
    ) LIMIT 1
)
SELECT
    w.id, w.subject, w.body, w.gold, w.silver, w.copper, w.expires_at,
    sender.name AS sender_name, recipient.name AS recipient_name,
    i.name AS item_name, i.quality
FROM writing w
JOIN game_character sender ON w.sender_id = sender.id
JOIN game_character recipient ON w.recipient_id = recipient.id
LEFT JOIN writing_items wi ON w.id = wi.writing_id
LEFT JOIN item i ON wi.item_id = i.id
WHERE recipient.id = (SELECT id FROM selected_character)
  AND w.expires_at > CURRENT_TIMESTAMP
ORDER BY w.expires_at DESC;

-- Query 7: Medium selectivity - Top mobs by loot value
-- Purpose: Find mobs with high-value loot (based on item quality and gold cost)
SELECT
    m.name, m.level_mob AS mob_level, l.name AS location_name,
    COUNT(DISTINCT ml.item_id) AS loot_count,
    SUM(i.gold + i.silver / 100.0 + i.copper / 10000.0) AS total_loot_value
FROM mob m
JOIN location l ON m.location_id = l.id
JOIN mob_loot ml ON m.id = ml.mob_id
JOIN item i ON ml.item_id = i.id
WHERE i.quality IN ('epic', 'legendary')
GROUP BY m.id, m.name, l.name
HAVING COUNT(DISTINCT ml.item_id) > 2
ORDER BY total_loot_value DESC;

-- Query 8: Low selectivity - Account collection summary
-- Purpose: Summarize mounts, pets, and toys owned by accounts
SELECT
    a.id, a.username,
    COUNT(DISTINCT am.mount_id) AS mount_count,
    COUNT(DISTINCT ap.pet_id) AS pet_count,
    COUNT(DISTINCT at.toy_id) AS toy_count,
    COUNT(DISTINCT c.id) AS character_count
FROM account a
LEFT JOIN game_character c ON a.id = c.account_id
LEFT JOIN account_mount am ON a.id = am.account_id
LEFT JOIN account_pet ap ON a.id = ap.account_id
LEFT JOIN account_toy at ON a.id = at.account_id
GROUP BY a.id, a.username
ORDER BY (COUNT(DISTINCT am.mount_id) + COUNT(DISTINCT ap.pet_id) + COUNT(DISTINCT at.toy_id)) DESC;

-- Query 9: High selectivity - Character abilities by specialization
-- Purpose: Get abilities for a specific character's specialization, class, and race
WITH selected_character AS (
    SELECT id FROM game_character LIMIT 1
)
SELECT
    c.name, a.name AS ability_name, a.type, a.cooldown,
    s.source
FROM game_character c
JOIN character_ability ca ON c.id = ca.character_id
JOIN ability a ON ca.ability_id = a.id
LEFT JOIN specialization_ability sa ON a.id = sa.ability_id
LEFT JOIN specialization sp ON sa.specialization_id = sp.id
LEFT JOIN class_ability cla ON a.id = cla.ability_id
LEFT JOIN class cl ON cla.class_id = cl.id
LEFT JOIN race_ability ra ON a.id = ra.ability_id
LEFT JOIN race r ON ra.race_id = r.id
CROSS JOIN LATERAL (
    SELECT COALESCE(sp.name, cl.name, r.name, 'Other') AS source
) s
WHERE c.id = (SELECT id FROM selected_character)
ORDER BY a.name;

-- Query 10: High selectivity - Specific character's bank and inventory
-- Purpose: Get all items in a character's bank and inventory
WITH selected_character AS (
    SELECT id FROM game_character LIMIT 1
)
SELECT
    c.name, i.name AS item_name, i.quality, i.item_level,
    COALESCE(ii.quantity, b.quantity) AS quantity,
    CASE WHEN ii.id IS NOT NULL THEN 'inventory' ELSE 'bank' END AS storage
FROM game_character c
LEFT JOIN inventory_items ii ON c.id = ii.character_id
LEFT JOIN bags bg ON ii.bag_id = bg.id
LEFT JOIN bank b ON c.id = b.character_id
JOIN item i ON i.id = COALESCE(ii.item_id, b.item_id)
WHERE c.id = (SELECT id FROM selected_character)
ORDER BY i.item_level DESC;

-- Query 11: Low selectivity - Item distribution by expansion
-- Purpose: Analyze item distribution across expansions
SELECT
    e.name AS expansion_name, i.quality,
    COUNT(DISTINCT i.id) AS item_count,
    AVG(i.item_level) AS avg_item_level
FROM item i
JOIN expansion e ON i.expansion_id = e.id
LEFT JOIN character_equipment ce ON i.id = ce.item_id
LEFT JOIN inventory_items ii ON i.id = ii.item_id
LEFT JOIN bank b ON i.id = b.item_id
GROUP BY e.name, i.quality
ORDER BY item_count DESC;