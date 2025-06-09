DROP TRIGGER IF EXISTS trg_validate_bag_item ON bags;
DROP TRIGGER IF EXISTS weapon_item_class_trigger ON weapon;
DROP TRIGGER IF EXISTS armor_item_class_trigger ON armor;
DROP TRIGGER IF EXISTS consumable_item_class_trigger ON consumable;
DROP TRIGGER IF EXISTS trade_goods_item_class_trigger ON trade_goods;
DROP TRIGGER IF EXISTS quest_item_class_trigger ON quest_item;
DROP TRIGGER IF EXISTS container_item_class_trigger ON container;
DROP TRIGGER IF EXISTS auction_lot_binding_type_trigger ON auction_lot;

DROP FUNCTION IF EXISTS
  validate_bag_item, validate_weapon_item_class, validate_armor_item_class,
  validate_consumable_item_class, validate_trade_goods_item_class,
  validate_quest_item_class, validate_container_item_class,
  validate_auction_binding_type;
