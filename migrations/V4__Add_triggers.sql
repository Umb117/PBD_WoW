CREATE OR REPLACE FUNCTION validate_bag_item()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.item_id IS NOT NULL AND (
        SELECT item_class
        FROM item
        WHERE id = NEW.item_id
    ) != 'container' THEN
        RAISE EXCEPTION 'Предмет в слоте сумки должен быть контейнером (item_class = container)';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_trigger
        WHERE tgname = 'trg_validate_bag_item'
    ) THEN
        CREATE TRIGGER trg_validate_bag_item
        BEFORE INSERT OR UPDATE ON bags
        FOR EACH ROW EXECUTE FUNCTION validate_bag_item();
    END IF;
END $$;


--item.item_class должен быть 'weapon' для записей, связанных с weapon
CREATE OR REPLACE FUNCTION validate_weapon_item_class()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT item_class FROM item WHERE id = NEW.id) != 'weapon' THEN
        RAISE EXCEPTION 'Item class must be "weapon" for weapon table';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_trigger
        WHERE tgname = 'weapon_item_class_trigger'
    ) THEN
        CREATE TRIGGER weapon_item_class_trigger
        BEFORE INSERT OR UPDATE ON weapon
        FOR EACH ROW EXECUTE FUNCTION validate_weapon_item_class();
    END IF;
END $$;


--item.item_class должен быть 'armor' для записей, связанных с armor
CREATE OR REPLACE FUNCTION validate_armor_item_class()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT item_class FROM item WHERE id = NEW.id) != 'armor' THEN
        RAISE EXCEPTION 'Item class must be "armor" for armor table';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_trigger
        WHERE tgname = 'armor_item_class_trigger'
    ) THEN
        CREATE TRIGGER armor_item_class_trigger
        BEFORE INSERT OR UPDATE ON armor
        FOR EACH ROW EXECUTE FUNCTION validate_armor_item_class();
    END IF;
END $$;


-- item.item_class должен быть 'consumable' для записей, связанных с consumable
CREATE OR REPLACE FUNCTION validate_consumable_item_class()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT item_class FROM item WHERE id = NEW.id) != 'consumable' THEN
        RAISE EXCEPTION 'Item class must be "consumable" for consumable table';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_trigger
        WHERE tgname = 'consumable_item_class_trigger'
    ) THEN
        CREATE TRIGGER consumable_item_class_trigger
        BEFORE INSERT OR UPDATE ON consumable
        FOR EACH ROW EXECUTE FUNCTION validate_consumable_item_class();
    END IF;
END $$;


--item.item_class должен быть 'trade_goods' для записей, связанных с trade_goods
CREATE OR REPLACE FUNCTION validate_trade_goods_item_class()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT item_class FROM item WHERE id = NEW.id) != 'trade_goods' THEN
        RAISE EXCEPTION 'Item class must be "trade_goods" for trade_goods table';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_trigger
        WHERE tgname = 'trade_goods_item_class_trigger'
    ) THEN
        CREATE TRIGGER trade_goods_item_class_trigger
        BEFORE INSERT OR UPDATE ON trade_goods
        FOR EACH ROW EXECUTE FUNCTION validate_trade_goods_item_class();
    END IF;
END $$;


CREATE OR REPLACE FUNCTION validate_quest_item_class()
RETURNS TRIGGER AS $$
BEGIN
    -- Проверка существования записи в item и соответствия item_class
    IF NOT EXISTS (
        SELECT 1
        FROM item
        WHERE id = NEW.id
          AND item_class = 'quest_item'
    ) THEN
        RAISE EXCEPTION 'Item class must be "quest_item" for quest_item table';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_trigger
        WHERE tgname = 'quest_item_class_trigger'
    ) THEN
        CREATE TRIGGER quest_item_class_trigger
        BEFORE INSERT OR UPDATE ON quest_item
        FOR EACH ROW EXECUTE FUNCTION validate_quest_item_class();
    END IF;
END $$;


CREATE OR REPLACE FUNCTION validate_container_item_class()
RETURNS TRIGGER AS $$
BEGIN
    -- Проверка существования записи в item и соответствия item_class
    IF NOT EXISTS (
        SELECT 1
        FROM item
        WHERE id = NEW.id
          AND item_class = 'container'
    ) THEN
        RAISE EXCEPTION 'Item class must be "container" for container table';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_trigger
        WHERE tgname = 'container_item_class_trigger'
    ) THEN
        CREATE TRIGGER container_item_class_trigger
        BEFORE INSERT OR UPDATE ON container
        FOR EACH ROW EXECUTE FUNCTION validate_container_item_class();
    END IF;
END $$;


CREATE OR REPLACE FUNCTION validate_auction_binding_type()
RETURNS TRIGGER AS $$
BEGIN
    -- Проверка, что связанный предмет не имеет binding_type = 'BoP'
    IF EXISTS (
        SELECT 1
        FROM item
        WHERE id = NEW.item_id
          AND binding_type = 'BoP'
    ) THEN
        RAISE EXCEPTION 'Item with binding_type "BoP" cannot be placed in auction';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_trigger
        WHERE tgname = 'auction_lot_binding_type_trigger'
    ) THEN
        CREATE TRIGGER auction_lot_binding_type_trigger
        BEFORE INSERT OR UPDATE OF item_id ON auction_lot
        FOR EACH ROW EXECUTE FUNCTION validate_auction_binding_type();
    END IF;
END $$;