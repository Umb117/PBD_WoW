# M3205_SerebrennikovaES

### Общие требования  
* Система должна обеспечивать хранение, обновление и синхронизацию данных об аккаунте игрока, его персонажах и связанных сущностях  

---

### Персонаж  

**Создание персонажа:**  
* Уникальное имя, задаваемое игроком при создании  
* Выбор сервера, задаваемый игроком при создании  
* Выбор класса, расы и пола при создании  
* Выбор специализации из доступных для класса  

**Настройки игрового процесса:**  
* Возможность выбора и изменения сложности рейдов и подземелий  
* Сохранение и обновление текущих талантов  
* Выбор двух профессий с отслеживанием их прогресса  

**Хранение данных:**  
* Текущий уровень и накопленный опыт  
* Снаряжение персонажа (обновляется в реальном времени)  
* Привязка к дополнению игры в соответствии с уровнем  
* Текущая локация персонажа (сохраняется при выходе из игры)  

**Экономика и инвентаризация:**  
* Валюты (золото, валюта фракций и т.д.)  
* Инвентарь, банк и почта (хранение писем, вложеных предметов)  
* Участие в аукционе (выставление, выкуп товаров, включая лоты с длительным хранением)  

**Социальные взаимодействия:**  
* Возможность вступления в гильдию  
* Управление квестами (взятие, завершение/отказ)  

**Прогресс и репутация:**  
* Репутация с различными фракциями  
* Общее и сессионное время в игре  

---

### Аккаунт  

**Учетные данные и безопасность:**  
* Видимое другим игрокам имя аккаунта  
* Хранение пароля в хэшированном виде  
* Привязка электронной почты  
* Возможность привязки телефона  
* История входов (IP-адреса, время, устройства)  
* История изменений пароля и персональных данных  

**Персональная информация:**  
* Страна проживания, дата рождения, настоящее имя и фамилия владельца  

**Управление подпиской:**  
* Статус подписки (активная/неактивная, тип)  

**Игровые сущности:**  
* Принадлежащие аккаунту персонажи  
* Коллекции: транспорт, питомцы, игрушки  
* Список званий и достижений  

**Социальные функции:**  
* Список друзей и игнорируемых игроков  
* Участие в сообществах (чаты, видимые на уровне аккаунта)  

---

## Основные сущности

**Персонаж (character)**
| Поле                   | Тип                         | Описание                                                                 |
|------------------------|-----------------------------|-------------------------------------------------------------------------|
| id                     | UUID (PRIMARY KEY)          | Уникальный идентификатор                                               |
| account_id             | UUID (FOREIGN KEY)          | Ссылка на аккаунт (`account.id`)                                       |
| name                   | VARCHAR(12) UNIQUE          | Имя персонажа (уникальное)                                             |
| gender                 | ENUM('male', 'female')      | Пол                                                                     |
| race_id                | UUID (FOREIGN KEY)          | Ссылка на расу (`race.id`)                                             |
| class_id               | UUID (FOREIGN KEY)          | Ссылка на класс (`class.id`)                                           |
| spec_id                | UUID (FOREIGN KEY)          | Ссылка на специализацию (`specialization.id`)                          |
| server_id              | UUID (FOREIGN KEY)          | Ссылка на сервер (`server.id`)                                         |
| expansion_id           | UUID (FOREIGN KEY)          | Текущее дополнение (`expansion.id`)                                    |
| location_id            | UUID (FOREIGN KEY)          | Текущая локация (`location.id`)                                        |
| gold                   | INT DEFAULT 0               | Золотые монеты игрока                                                  |
| silver                 | INT DEFAULT 0               | Серебряные монеты игрока                                               |
| copper                 | INT DEFAULT 0               | Маедные монеты игрока                                                  |
| total_playtime         | INTERVAL                    | Общее время в игре                                                     |
| session_playtime       | INTERVAL                    | Время текущей сессии                                                   |
| total_exp_gained       | INT                         | Всего получено опыта                                                   |

**Аккаунт (account)**
| Поле            | Тип                | Описание                                  |
|-----------------|--------------------|------------------------------------------|
| id	              | UUID (PRIMARY KEY)	    | Уникальный идентификатор        |
| username	          | VARCHAR(12)             | Видимое имя (никнейм)           |
| password_hash       |	VARCHAR(255)	        | Хэш пароля (bcrypt)             |
| email               |	VARCHAR(255) UNIQUE     | Электронная почта               |
| phone	              | VARCHAR(20) UNIQUE NULL | Телефон (с кодом страны)        |
| real_name	          | VARCHAR(255)	        | Настоящее имя                   |
| birth_date	      | DATE	                | Дата рождения                   |
| country_code	      | CHAR(2)	                | Код страны (ISO 3166-1 alpha-2) |
| subscription_status |	ENUM('active', 'inactive') | Статус подписки |
| subscription_end	  | TIMESTAMP	| Дата окончания подписки |


**Сервер (server)**
| Поле          | Тип                | Описание                  |
|---------------|--------------------|--------------------------|
| id            | UUID (PRIMARY KEY) | Уникальный ID сервера    |
| name          | VARCHAR(64) UNIQUE | Название ("Гордунни")    |
| region        | ENUM('EU', 'US', 'ASIA') | Регион сервера      |

**Дополнение (expansion)**
| Поле          | Тип                | Описание                                  |
|---------------|--------------------|------------------------------------------|
| id            | UUID (PRIMARY KEY) | Уникальный ID                            |
| name          | VARCHAR(255)       | Название ("Legion" и т.д.)               |
| min_level     | INT                | Минимальный уровень                      |
| max_level     | INT                | Максимальный уровень                     |

**Класс (class)**
| Поле          | Тип                | Описание                                  |
|---------------|--------------------|------------------------------------------|
| id            | UUID (PRIMARY KEY) | Уникальный ID                            |
| name          | VARCHAR(32)        | Название класса                          |
| description   | TEXT               | Описание                                 |

**Раса (race)**
| Поле               | Тип                | Описание                                  |
|--------------------|--------------------|------------------------------------------|
| id                 | UUID (PRIMARY KEY) | Уникальный ID                            |
| name               | VARCHAR(64)        | Название расы                            |
| starting_zone_id   | UUID (FOREIGN KEY) | Ссылка на начальную локацию              |

**Специализация (specialization)**
| Поле          | Тип                | Описание                                  |
|---------------|--------------------|------------------------------------------|
| id            | UUID (PRIMARY KEY) | Уникальный ID                            |
| name          | VARCHAR(64)        | Название специализации                   |
| class_id      | UUID (FOREIGN KEY) | Ссылка на класс                          |
| role          | ENUM('tank', 'dps', 'healer') | Роль в группе                 |

**Способность (ability)**
| Поле              | Тип                       | Описание                                  |
|-------------------|---------------------------|------------------------------------------|
| id                | UUID (PRIMARY KEY)        | Уникальный ID                            |
| name              | VARCHAR(64)               | Название способности                     |
| description       | TEXT                      | Описание                                 |
| type              | ENUM('passive', 'active') | Тип способности                          |
| cast_time         | FLOAT                     | Время применения (сек)                   |
| resource          | ENUM('mana', 'energy', 'rage', 'combo_points') | Ресурс              |
| range             | FLOAT                     | Дальность действия (метры)               |
| cooldown          | FLOAT                     | Время восстановления (сек)               |

**Предмет (item)**
| Поле           | Тип                | Описание                                  |
|----------------|--------------------|------------------------------------------|
| id             | UUID (PRIMARY KEY) | Уникальный ID                            |
| name           | VARCHAR(255)       | Название предмета                        |
| item_level     | INT                | Уровень предмета (ilvl)                  |
| quality        | ENUM('common', 'uncommon', 'rare', 'epic', 'legendary', 'artifact') | Качество |
| max_stack      | INT DEFAULT 1      | Макс. количество в стаке                 |
| gold           | INT DEFAULT 0      | Цена продажи NPC (часть золотых монет) |
| silver         | INT DEFAULT 0      | Цена продажи NPC (часть серебряных монет) |
| copper         | INT DEFAULT 0      | Цена продажи NPC (часть медных монет) |
| description    | TEXT               | Описание                                 |
| expansion_id   | UUID (FOREIGN KEY) | Ссылка на дополнение                     |
| item_class     | ENUM('weapon', 'armor', 'consumable', 'trade_goods', 'quest_item', 'container') | Категория |
| binding_type   | ENUM('BoP', 'BoE', 'BtA') NULL | Тип привязки                 |
| required_level | INT DEFAULT 0      | Минимальный уровень                      |

Категории предметов (расширяют item через CTI (Class Table Inheritance))

Создание унаследованного класса
```sql
   -- 1. Создаем запись в родительской таблице
   INSERT INTO item (id, name, item_class, quality, required_level...)
   VALUES (
       'weapon_123', 
       'Меч Тьмы', 
       'weapon', 
       'epic', 
       60
       ...
   );

   -- 2. Создаем запись в дочерней таблице
   INSERT INTO weapon (id, damage_min, damage_max, attack_speed, weapon_type, handedness...)
   VALUES (
       'weapon_123', 
       150, 
       200, 
       2.5, 
       'sword', 
       'two-handed'
       ...
   );
```
Проверка целостности:
```sql
item.item_class должен быть 'weapon' для записей, связанных с weapon
CREATE OR REPLACE FUNCTION validate_weapon_class()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.item_class != 'weapon' THEN
        RAISE EXCEPTION 'Item class должен быть "weapon"';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validate_weapon_class
BEFORE INSERT OR UPDATE ON item
FOR EACH ROW 
WHEN (NEW.item_class = 'weapon')
EXECUTE FUNCTION validate_weapon_class();
```

**Броня (armor)**
| Поле          | Тип                | Описание                                  |
|---------------|--------------------|------------------------------------------|
| id `armor.id = item.id` | UUID (PRIMARY KEY) | Уникальный ID (совпадает с `item.id`) |
| durability    | INT                | Прочность                                |
| armor_type    | ENUM('cloth', 'leather', 'mail', 'plate') | Тип брони          |
| armor_value   | INT                | Значение брони                          |
| slot          | ENUM('head', 'shoulders', 'chest', 'hands', 'legs', 'feet', 'back', 'waist', 'wrist', 'neck', 'finger', 'trinket', 'tabard', 'shirt') | Слот |

**Оружие (weapon)**
| Поле          | Тип                | Описание                                  |
|---------------|--------------------|------------------------------------------|
| id `weapon.id = item.id` | UUID (PRIMARY KEY) | Уникальный ID (совпадает с `item.id`) |
| durability    | INT                | Прочность                                |
| damage_min    | INT                | Минимальный урон                         |
| damage_max    | INT                | Максимальный урон                        |
| attack_speed  | FLOAT              | Скорость атаки                           |
| weapon_type   | ENUM('sword', 'axe', 'dagger', 'shield', 'staff', 'mace', 'fist', 'bow', 'gun', 'polearm', 'wand') | Тип оружия |
| handedness    | ENUM('one-handed', 'two-handed') | Одно/двуручное        |

**Расходуемые (consumable)**
| Поле          | Тип                | Описание                                  |
|---------------|--------------------|------------------------------------------|
| id `consumable.id = item.id` | UUID (PRIMARY KEY) | Уникальный ID (совпадает с `item.id`) |
| effect        | ENUM('heal', 'mana', 'buff', 'food', 'potion', 'elixir', 'scroll') | Тип эффекта |
| duration      | INT                | Длительность эффекта (сек)               |
| cooldown      | INT                | Время восстановления (сек)               |
| charges       | INT DEFAULT 1      | Количество использований                 |
| required_level| INT DEFAULT 0      | Минимальный уровень                      |

**Профессиональные ресурсы (trade_goods)**
| Поле          | Тип                | Описание                                  |
|---------------|--------------------|------------------------------------------|
| id `trade_goods.id = item.id` | UUID (PRIMARY KEY) | Уникальный ID (совпадает с `item.id`) |
| profession_id | UUID (FOREIGN KEY) | Ссылка на профессию    

**Квестовые предметы (quest_item)**
| Поле          | Тип                | Описание                                  |
|---------------|--------------------|------------------------------------------|
| id `quest_item.id = item.id` | UUID (PRIMARY KEY) | Уникальный ID (совпадает с `item.id`) |
| quest_id      | UUID (PRIMARY KEY) | Связанный квест                          |
| is_quest_start| BOOLEAN            | Можно ли начать квест через предмет      |

**Контейнеры (container)**
| Поле          | Тип                | Описание                                  |
|---------------|--------------------|------------------------------------------|
| id `container.id = item.id` | UUID (PRIMARY KEY) | Уникальный ID (совпадает с `item.id`) |
| size          | INT                | Количество слотов                        |

**Локация (location)**
| Поле          | Тип                | Описание                                  |
|---------------|--------------------|------------------------------------------|
| id            | UUID (PRIMARY KEY) | Уникальный ID                            |
| name          | VARCHAR(64)        | Название локации                         |
| expansion_id  | UUID (FOREIGN KEY) | Ссылка на дополнение                     |

**Профессия (profession)**
| Поле          | Тип                | Описание                                  |
|---------------|--------------------|------------------------------------------|
| id            | UUID (PRIMARY KEY) | Уникальный ID профессии                  |
| name          | VARCHAR(64)        | Название (Кузнечное дело, Травничество и т.д.) |

**Рецепт (recipe)**
| Поле               | Тип                | Описание                                  |
|--------------------|--------------------|------------------------------------------|
| id                 | UUID (PRIMARY KEY) | Уникальный ID рецепта                    |
| name               | VARCHAR(128)       | Название рецепта                         |
| expansion_id       | UUID (FOREIGN KEY) | Дополнение, в котором добавлен рецепт    |
| profession_id      | UUID (FOREIGN KEY) | Ссылка на профессию                      |
| result_item_id     | UUID (FOREIGN KEY) | Создаваемый предмет                      |
| required_skill     | INT                | Требуемый уровень навыка профессии       |

**Гильдия (guild)**
| Поле          | Тип                     | Описание                                  |
|---------------|-------------------------|------------------------------------------|
| id            | UUID (PRIMARY KEY)      | Уникальный идентификатор                 |
| name          | VARCHAR(24) UNIQUE      | Название гильдии                         |
| description   | TEXT                    | Описание гильдии                         |
| type          | ENUM('PvE','PvP','RP','mixed') | Тип гильдии                  |

**Сообщество (community)**
| Поле          | Тип                     | Описание                                  |
|---------------|-------------------------|------------------------------------------|
| id            | UUID (PRIMARY KEY)      | Уникальный идентификатор                 |
| name          | VARCHAR(24) UNIQUE      | Название сообщества                      |
| description   | TEXT                    | Описание сообщества                      |

**Задание (quest)**
| Поле          | Тип                     | Описание                                  |
|---------------|-------------------------|------------------------------------------|
| id            | UUID (PRIMARY KEY)      | Уникальный идентификатор                 |
| name          | VARCHAR(128)            | Название квеста                          |
| description   | TEXT                    | Текст задания                            |
| gold          | INT DEFAULT 0           | Денежная награда (часть золотых монет)   |
| silver        | INT DEFAULT 0           | Денежная награда (часть серебряных монет) |
| copper        | INT DEFAULT 0           | Денежная награда (часть медных монет)    |

**Цель (objective)**
| Поле          | Тип                     | Описание                                  |
|---------------|-------------------------|------------------------------------------|
| id            | UUID (PRIMARY KEY)      | Уникальный идентификатор                 |
| type          | ENUM('kill','collect','use') | Тип цели                            |
| target_mob_id | UUID (FOREIGN KEY)      | Цель (ID моба)                           |
| target_item_id | UUID (FOREIGN KEY)     | Цель (ID предмета)                       |
| quantity      | INT                     | Требуемое количество                     |
| quest_id      | UUID (FOREIGN KEY)      | Ссылка на квест                          |

- `target_mob_id` — для целей типа **"убить"** (ссылка на таблицу мобов).
- `target_item_id` — для целей типа **"собрать"** (ссылка на таблицу предметов).
- Поле `type` определяет, какое из полей (`target_mob_id` или `target_item_id`) должно быть заполнено.

_Необходимо добавить CHECK-ограничение, чтобы только одно из полей было заполнено:_
```
CONSTRAINT chk_target_type 
        CHECK (
            (type = 'kill' AND target_mob_id IS NOT NULL AND target_item_id IS NULL) OR
            (type = 'collect' AND target_item_id IS NOT NULL AND target_mob_id IS NULL)
        )
```

**Подземелье (dungeon)**
| Поле          | Тип                     | Описание                                  |
|---------------|-------------------------|------------------------------------------|
| id            | UUID (PRIMARY KEY)      | Уникальный идентификатор                 |
| name          | VARCHAR(64) UNIQUE      | Название подземелья                      |
| location_id   | UUID (FOREIGN KEY)      | Локация                                  |
| expansion_id  | UUID (FOREIGN KEY)      | Ссылка на дополнение                     |

**Рейд (raid)**
| Поле          | Тип                     | Описание                                  |
|---------------|-------------------------|------------------------------------------|
| id            | UUID (PRIMARY KEY)      | Уникальный идентификатор                 |
| name          | VARCHAR(64) UNIQUE      | Название рейда                           |
| location_id   | UUID (FOREIGN KEY)      | Локация                                  |
| expansion_id  | UUID (FOREIGN KEY)      | Ссылка на дополнение                     |

**Моб (mob)**
| Поле          | Тип                     | Описание                                  |
|---------------|-------------------------|------------------------------------------|
| id            | UUID (PRIMARY KEY)      | Уникальный идентификатор                 |
| name          | VARCHAR(64) UNIQUE      | Название моба                            |
| location_id   | UUID (FOREIGN KEY)      | Локация                                  |
| is_boss       | BOOL                    | Является ли боссом                       |
| level         | INT                     | Уровень моба                             |

**Валюта (currency)**
| Поле          | Тип                | Описание                     |
|---------------|--------------------|-----------------------------|
| id            | UUID (PRIMARY KEY) | Уникальный ID валюты        |
| name          | VARCHAR(64)        | Название                    |
| expansion_id  | UUID (FOREIGN KEY) | Дополнение                  |

**Репутация с фракциями (reputation)**
| Поле          | Тип                | Описание                     |
|---------------|--------------------|-----------------------------|
| id            | UUID (PRIMARY KEY) | Уникальный ID фракции       |
| name          | VARCHAR(64)        | Название фракции            |
| expansion_id  | UUID (FOREIGN KEY) | Дополнение                  |

**Транспорт (mount)**
| Поле          | Тип                | Описание                     |
|---------------|--------------------|-----------------------------|
| id            | UUID (PRIMARY KEY) | Уникальный ID транспорта    |
| name          | VARCHAR(64)        | Название                    |
| type          | ENUM('flying', 'ground', 'aquatic') | Тип |

**Питомцы (pet)**
| Поле          | Тип                | Описание                     |
|---------------|--------------------|-----------------------------|
| id            | UUID (PRIMARY KEY) | Уникальный ID питомца       |
| name          | VARCHAR(64)        | Название                    |
| pet_type      | ENUM('humanoid', 'beast', 'aquatic', 'magical', 'mechanical', 'dragonkin', 'undead', 'elemental', 'flying') | Тип |
| quality       | ENUM('poor', 'common', 'uncommon', 'rare') | Качество |

**Игрушки (toy)**
| Поле          | Тип                | Описание                     |
|---------------|--------------------|-----------------------------|
| id            | UUID (PRIMARY KEY) | Уникальный ID игрушки       |
| name          | VARCHAR(64)        | Название                    |
| description   | TEXT               | Описание                    |

**Звания (title)**
| Поле          | Тип                | Описание                     |
|---------------|--------------------|-----------------------------|
| id            | UUID (PRIMARY KEY) | Уникальный ID звания        |
| name          | VARCHAR(64)        | Название                    |

**Письмо (writing)**
| Поле          | Тип                | Описание                     |
|---------------|--------------------|-----------------------------|
| id            | UUID (PRIMARY KEY) | Уникальный ID письма        |
| sender_id     | UUID (FOREIGN KEY) | ID отправителя              |
| recipient_id  | UUID (FOREIGN KEY) | ID получателя               |
| subject       | VARCHAR(40)        | Тема                        |
| body          | TEXT               | Текст                       |
| gold           | INT DEFAULT 0      | Приложенные деньги (часть золотых монет) |
| silver         | INT DEFAULT 0      | Приложенные деньги (часть серебряных монет) |
| copper         | INT DEFAULT 0      | Приложенные деньги (часть медных монет) |
| cod           | BOOL               | Это наложенный платеж       |
| expires_at    | TIMESTAMP          | Время удаления (текущее время + 30 дней) |

**Лот аукциона (auction_lot)**
| Поле          | Тип                | Описание                     |
|---------------|--------------------|-----------------------------|
| id            | UUID (PRIMARY KEY) | Уникальный ID лота          |
| character_id  | UUID (FOREIGN KEY) | ID персонажа
| item_id       | UUID (FOREIGN KEY) | ID предмета                 |
| quantity      | INT                | Количество                  |
| gold          | INT DEFAULT 0      | Цена (начальная если это торги, и конечная если выкуп) (часть золотых монет) |
| silver        | INT DEFAULT 0      | Цена (начальная если это торги, и конечная если выкуп) (часть серебряных монет) |
| copper        | INT DEFAULT 0      | Цена (начальная если это торги, и конечная если выкуп) (часть медных монет) |
| buyout_mode   | BOOL               | Режим выкупа                |
| expires_at    | TIMESTAMP          | Время окончания торгов      |

Добавить CHECK-ограничение или триггер, проверяющий, что выставляемая вещь не персональная.

## Вспомогательные таблицы:

### Связанные с аккаунтом:

**История входов (login_history)**
| Поле            | Тип                | Описание                                  |
|-----------------|--------------------|------------------------------------------|
| account_id    | UUID (FOREIGN KEY) | ID аккаунта                                |
| ip_address    | INET               | IP-адрес                                   |
| login_time    | TIMESTAMP          | Время входа                                |
| device_info	| JSONB              | {"os": "Windows", "browser": "Chrome"}     |

**История изменений (account_history)**
| Поле            | Тип                | Описание                                  |
|-----------------|--------------------|------------------------------------------|
| account_id    | UUID (FOREIGN KEY) | ID аккаунта                                |
| changed_field | VARCHAR(64)        | Измененное поле (password, email и т.д.)   |
| old_value     | TEXT               | Старое значение                            |
| new_value	    | TEXT               | Новое значение                             |
| changed_at	| TIMESTAMP          | Время изменения                            |

**Друзья (account_friend)**
| Поле            | Тип                | Описание                                  |
|-----------------|--------------------|------------------------------------------|
| account_id      | UUID (FOREIGN KEY) | ID основного аккаунта                    |
| friend_id       | UUID (FOREIGN KEY) | ID аккаунта друга                        |
| since           | TIMESTAMP          | Дата добавления                          |
| note            | VARCHAR(128)       | Произвольная заметка                     |

**Игнорируемые (account_ignore)**
| Поле            | Тип                | Описание                                  |
|-----------------|--------------------|------------------------------------------|
| account_id      | UUID (FOREIGN KEY) | ID основного аккаунта                    |
| ignored_id      | UUID (FOREIGN KEY) | ID игнорируемого аккаунта                |
| created_at      | TIMESTAMP          | Дата добавления                          |

**Сообщество аккаунта (community_account)**
| Поле          | Тип                     | Описание                                  |
|---------------|-------------------------|------------------------------------------|
| account_id    | UUID (FOREIGN KEY)      | ID аккаунта                             |
| community_id  | UUID (FOREIGN KEY)      | ID сообщест                             |

### Связанные с игровыми коллекциями в аккаунте

**Транспорт игрока (account_mount)**
| Поле          | Тип                | Описание                     |
|---------------|--------------------|-----------------------------|
| account_id  | UUID (FOREIGN KEY) | ID аккаунта                |
| mount_id      | UUID (FOREIGN KEY) | ID транспорта               |

**Питомцы игрока (account_pet)**
| Поле          | Тип                | Описание                     |
|---------------|--------------------|-----------------------------|
| account_id  | UUID (FOREIGN KEY) | ID аккаунта                |
| pet_id        | UUID (FOREIGN KEY) | ID питомца                  |

**Игрушки игрока (account_toy)**
| Поле          | Тип                | Описание                     |
|---------------|--------------------|-----------------------------|
| account_id  | UUID (FOREIGN KEY) | ID аккаунта                |
| toy_id        | UUID (FOREIGN KEY) | ID игрушки                  |

**Звания игрока (account_title)**
| Поле          | Тип                | Описание                     |
|---------------|--------------------|-----------------------------|
| account_id  | UUID (FOREIGN KEY) | ID аккаунта                |
| title_id      | UUID (FOREIGN KEY) | ID звания                   |

### Связанные с хранением предметов персонажа:

**Экипировка (character_equipment)**
| Поле             | Тип                | Описание                                  |
|------------------|--------------------|------------------------------------------|
| character_id     | UUID (FOREIGN KEY) | Ссылка на персонажа                      |
| slot_type        | ENUM               | Тип слота (голова, грудь, шея и т.д.)    |
| item_id          | UUID (FOREIGN KEY) | Ссылка на предмет (NULL если слот пуст)  |
| equipped_at      | TIMESTAMP          | Время экипировки                        |

**ENUM `slot_type` (18 значений):**
```sql
CREATE TYPE equipment_slot AS ENUM (
  'head', 'neck', 'shoulders', 'chest', 'back', 
  'wrists', 'hands', 'waist', 'legs', 'feet', 
  'finger_1', 'finger_2', 'trinket_1', 'trinket_2', 
  'main_hand', 'off_hand', 'tabard', 'shirt'
);
```
Также нужно поставить триггер на создание персонажа, который создает 18 слотов снаряжения с каждым из типов.  
И запретить удалять записи и менять тип слота экипировки, а так же проверять что ссылка на предмет ведет на предмет брони

**Рюкзак и сумки (bags) (ячейки под предмет-сумки)**
| Поле          | Тип                | Описание                                  |
|---------------|--------------------|------------------------------------------|
| id            | UUID (PRIMARY KEY) | Уникальный ID сумки                      |
| character_id  | UUID (FOREIGN KEY) | Владелец                                 |
| slot          | INT                | Слот (0-4, 0 = базовый рюкзак)           |
| item_id       | UUID (FOREIGN KEY) NULL | Ссылка на предмет-сумку                 |
| size          | INT                | Количество слотов (16 для базового)      |

Необходима настройка: при создании персонажа создается 5 сумок, где одна из них базовый рюкзак.  
Удалять сумки (ячейки под предмет-сумки) запрещено.
Добавить CHECK-ограничение или триггер, проверяющий, что item.item_class = 'container'.

**Предметы в инвентаре (inventory_items)**
| Поле          | Тип                | Описание                                  |
|---------------|--------------------|------------------------------------------|
| id            | UUID (PRIMARY KEY) | Уникальный ID записи                     |
| character_id  | UUID (FOREIGN KEY) | Владелец                                 |
| bag_id        | UUID (FOREIGN KEY) | Сумка                                    |
| position      | INT                | Позиция в сумке (0-size)                 |
| item_id       | UUID (FOREIGN KEY) | Ссылка на предмет                        |
| quantity      | INT                | Количество                               |

**Банк персонажа (bank)**
| Поле            | Тип                | Описание                                  |
|-----------------|--------------------|------------------------------------------|
| character_id    | UUID (FOREIGN KEY) | ID персонажа                             |
| item_id         | UUID (FOREIGN KEY) | ID предмета                              |
| slot            | INT                | Номер ячейки (0-100)                     |
| quantity        | INT                | Количество                               |

**Вложенные предметы (writing_items)**
| Поле            | Тип                     | Описание                                  |
|-----------------|-------------------------|------------------------------------------|
| writing_id      | UUID (FOREIGN KEY)      | Письмо                                    |
| item_id         | UUID (FOREIGN KEY)      | Предмет                                  |

### Связанные с валютой, репутацией, гильдией персонажа:

**Валюта персонажа (character_currency)**
| Поле          | Тип                | Описание                     |
|---------------|--------------------|-----------------------------|
| character_id  | UUID (FOREIGN KEY) | ID персонажа                |
| currency_id   | UUID (FOREIGN KEY) | ID валюты                   |
| amount        | INT                | Количество                  |

**Репутация персонажа (character_reputation)**
| Поле          | Тип                | Описание                     |
|---------------|--------------------|-----------------------------|
| character_id  | UUID (FOREIGN KEY) | ID персонажа                |
| faction_id    | UUID (FOREIGN KEY) | ID фракции                  |
| level         | ENUM('hated', 'hostile', 'unfriendly', 'neutral', 'friendly', 'honored', 'revered', 'exalted') | Уровень |
| value         | INT                | Текущее значение репутации  |

**Гильдия персонажа (guild_character)**
| Поле          | Тип                     | Описание                                  |
|---------------|-------------------------|------------------------------------------|
| character_id  | UUID (FOREIGN KEY)      | ID персонажа                             |
| guild_id      | UUID (FOREIGN KEY)      | ID гильдии                               |
| player_rank   | ENUM('recruit', 'participant', 'veteran', 'officer', 'guild master') | Звание игрока в гильдии |

### Делящие `ability` на категории:

**Расовые способности (race_ability)**
| Поле          | Тип                | Описание                                  |
|---------------|--------------------|------------------------------------------|
| ability_id     | UUID (FOREIGN KEY) | ID способности                             |
| race_id        | UUID (FOREIGN KEY) | ID расы                               |

**Классовые способности (class_ability)**
| Поле          | Тип                | Описание                                  |
|---------------|--------------------|------------------------------------------|
| ability_id     | UUID (FOREIGN KEY) | ID способности                           |
| class_id        | UUID (FOREIGN KEY) | ID класса                               |

**Способности специализации (specialization_ability)**
| Поле          | Тип                | Описание                                  |
|---------------|--------------------|------------------------------------------|
| ability_id     | UUID (FOREIGN KEY) | ID способности                        |
| specialization_id  | UUID (FOREIGN KEY) | ID специализации                  |

**Способности мобов (mob_ability)**
| Поле          | Тип                | Описание                                  |
|---------------|--------------------|------------------------------------------|
| ability_id     | UUID (FOREIGN KEY) | ID способности                        |
| mob_id         | UUID (FOREIGN KEY) | ID моба                               |

**Способности персонажа (character_ability)**
| Поле            | Тип                | Описание                                  |
|-----------------|--------------------|------------------------------------------|
| character_id    | UUID (FOREIGN KEY) | ID персонажа                             |
| ability_id      | UUID (FOREIGN KEY) | ID способности                           |

### Связанные с рецептами и профессиями:

**Ингредиенты для рецепта (recipe_ingredients)**
| Поле           | Тип                | Описание                 |
|----------------|--------------------|-------------------------|
| recipe_id      | UUID (FOREIGN KEY) | Ссылка на рецепт        |
| item_id        | UUID (FOREIGN KEY) | Ингредиент              |
| quantity       | INT                | Количество              |

**Связь персонажа с рецептами (character_recipe)**
| Поле               | Тип                | Описание                                  |
|--------------------|--------------------|------------------------------------------|
| character_id       | UUID (FOREIGN KEY) | ID персонажа                             |
| recipe_id          | UUID (FOREIGN KEY) | ID рецепта                               |

_При попытке добавить рецепт (INSERT/UPDATE в character_recipe) триггер:_

* _Ищет профессию (profession_id), связанную с рецептом._
* _Проверяет, есть ли эта профессия у персонажа в character_profession_

``` sql
CREATE OR REPLACE FUNCTION check_recipe_profession()
RETURNS TRIGGER AS $$
BEGIN
    -- Проверяем, есть ли у персонажа профессия, связанная с рецептом
    IF NOT EXISTS (
        SELECT 1 
        FROM character_profession 
        WHERE 
            character_id = NEW.character_id 
            AND profession_id = (
                SELECT profession_id 
                FROM recipe 
                WHERE id = NEW.recipe_id
            )
    ) THEN
        RAISE EXCEPTION 'Персонаж не имеет нужной профессии для изучения рецепта';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Привязка триггера к таблице character_recipe
CREATE TRIGGER trg_recipe_profession_check
BEFORE INSERT OR UPDATE ON character_recipe
FOR EACH ROW EXECUTE FUNCTION check_recipe_profession();
```

**Прогресс профессии у персонажа (character_profession)**
| Поле               | Тип                | Описание                                  |
|--------------------|--------------------|------------------------------------------|
| character_id       | UUID (FOREIGN KEY) | ID персонажа                             |
| profession_id      | UUID (FOREIGN KEY) | ID профессии                             |
| skill_level        | INT DEFAULT 0      | Текущий уровень навыка (0-300)           |

Добавить триггер, который проверяет количество профессий перед вставкой, чтобы профессий было не больше 2

### Связанные с квестами

**Награда за квест (quest_rewards)**
| Поле          | Тип                     | Описание                                  |
|---------------|-------------------------|------------------------------------------|
| quest_id      | UUID (FOREIGN KEY)      | Квест                                    |
| item_id       | UUID (FOREIGN KEY)      | Предмет                                  |

**Прогресс целей квеста (character_quest_objectives)**
| Поле            | Тип                | Описание                                  |
|-----------------|--------------------|------------------------------------------|
| objective_id    | UUID (FOREIGN KEY) | ID цели                                  |
| character_quest_id  | UUID (FOREIGN KEY) | ID квеста из журнала заданий игрока |
| current         | INT                | Текущий прогресс (например, 3/5)        |

**Журнал заданий (character_quest)**
| Поле            | Тип                | Описание                                  |
|-----------------|--------------------|------------------------------------------|
| id              | UUID (PRIMARY KEY) | Уникальный идентификатор                 |
| character_id    | UUID (FOREIGN KEY) | ID персонажа                             |
| quest_id        | UUID (FOREIGN KEY) | ID квеста                                |
| status          | ENUM('active', 'completed', 'failed') | Статус               |

### Связывающие мобов с лутом и классы с расами

**Лут с моба (mob_loot)**
| Поле          | Тип                     | Описание                                  |
|---------------|-------------------------|------------------------------------------|
| mob_id        | UUID (FOREIGN KEY)      | Моб                                      |
| item_id       | UUID (FOREIGN KEY)      | Предмет                                  |
| chance        | FLOAT                   | Шанс выпадения                           |

**Доступные для класса расы (class_race)**
| Поле          | Тип                | Описание                                  |
|---------------|--------------------|------------------------------------------|
| class_id       | UUID (FOREIGN KEY) | ID класса                             |
| race_id        | UUID (FOREIGN KEY) | ID расы                               |

Добавить CHECK-ограничение или триггер, проверяющий, что отправляемая вещь не персональная.

### Характеристики брони/оружия

**Таблица характеристик брони/оружия (item_stats)**
| Поле         | Тип                 | Описание              | Ограничения                   |
|--------------|---------------------|-----------------------|------------------------------|
| item_id      | UUID                | ID предмета           | `FOREIGN KEY REFERENCES item(id)`    |
| stat_type    | ENUM('Intellect', 'Agility', 'Strength', 'Stamina', 'Armor', 'Critical Strike Chance', 'Haste', 'Mastery', 'Versatility', 'Speed', 'Leech', 'Avoidance') | Тип характеристики                                      |
| value        | INT           | Значение характеристики                                 |

Первичный ключ: `(item_id, stat_type)`  

## Отношения между сущностями:

#### 1. Аккаунт (account) → Персонажи (character)
**Тип связи**: Один-ко-многим  
У одного аккаунта несколько персонажей.  
У одного персонажа один аккаунт.  
**Внешний ключ**:  
`account.id` → `character.account_id`

#### 2. Персонаж (character) → Специализация (specialization)
**Тип связи**: Один-ко-многим  
У одного персонажа одна специальность.  
У одной специальности несколько персонажей.  
**Внешний ключ**:  
`character.spec_id` → `specialization.id`

#### 3. Персонаж (character) → Класс (class)
**Тип связи**: Один-ко-многим  
У одного персонажа один класс.  
У одного класса несколько персонажей.  
`character.class_id` → `class.id`  

#### 4. Класс (class) → Раса (race)
**Тип связи**: Многие-ко-многим (через `class_race`)  
У одного класса несколько рас.  
У одной расы несколько классов.  
`class.id` → `class_race.class_id`  
`race.id` → `class_race.race_id`  

#### 5. Персонаж (character) → Раса (race)
**Тип связи**: Один-ко-многим  
У одного персонажа одна раса.  
У одной расы несколько персонажей.  
`character.race_id` → `race.id`  

#### 6. Класс (class) → Специализация (specialization)
**Тип связи**: Один-ко-многим  
У одного класса несколько специализаций.  
У одной специализации один класс.  
`specialization.class_id` → `class.id`

#### 7. Персонаж (character) → Способности (ability)
**Тип связи**: Многие-ко-многим (через `character_ability`)  
У одного персонажа несколько способностей.  
У одной способности несколько персонажей.  
`character.id` → `character_ability.character_id`  
`ability.id` → `character_ability.ability_id`

#### 8. Раса (race) → Способности (ability)
**Тип связи**: Один-ко-многим (через `race_ability`)  
У одной расы несколько способностей.  
У одной способности одна раса (если она вообще расовая).  
`ability.id` → `race_ability.ability_id`  
`race.id` → `race_ability.race_id`

#### 9. Класс (class) → Способности (ability)
**Тип связи**: Один-ко-многим (через `class_ability`)  
У одного класса несколько способностей.  
У одной способности один класс (если она вообще классовая).  
`class.id` → `class_ability.character_id`  
`ability.id` → `class_ability.ability_id`

#### 10. Специализация (specialization) → Способности (ability)
**Тип связи**: Один-ко-многим (через `specialization_ability`)  
У одной специализации несколько способностей.  
У одной способности одна специализация (если она вообще относится к специализации).  
`specialization.id` → `specialization_ability.specialization_id`  
`ability.id` → `specialization_ability.ability_id`

#### 11. Моб (mob) → Способности (ability)
**Тип связи**: Многие-ко-многим (через `mob_ability`)  
У одного моба несколько способностей.  
У одной способности несколько мобов (если она вообще относится к мобу).  
`mob.id` → `mob_ability.mob_id`  
`ability.id` → `mob_ability.ability_id`

#### 12. Предмет (item) → Броня (armor)
**Тип связи**: Один-к-одному  
Наследование брони от предмета  
**Внешний ключ**:  
`armor.id` → `item.id`

#### 13. Предмет (item) → Оружие (weapon)
**Тип связи**: Один-к-одному  
Наследование оружия от предмета  
**Внешний ключ**:  
`weapon.id` → `item.id`

#### 14. Предмет (item) → Расходуемые (consumable)
**Тип связи**: Один-к-одному  
Наследование расходуемого от предмета  
**Внешний ключ**:  
`consumable.id` → `item.id`  

#### 15. Предмет (item) → Профессиональные ресурсы (trade_goods)
**Тип связи**: Один-к-одному  
Наследование профессионального ресурса от предмета  
**Внешний ключ**:  
`trade_goods.id` → `item.id`  

#### 16. Предмет (item) → Квестовые предметы (quest_item)
**Тип связи**: Один-к-одному  
Наследование квестового предмета от предмета  
**Внешний ключ**:  
`quest_item.id` → `item.id`

#### 17. Предмет (item) → Контейнеры (container)
**Тип связи**: Один-к-одному  
Наследование контейнера от предмета  
**Внешний ключ**:  
`container.id` → `item.id`

#### 18. Персонаж (character) → Сервер (server)
**Тип связи**: Один-ко-многим   
У одного персонажа один сервер.  
У одного сервера несколько персонажей.  
`character.server_id` → `server.id`

#### 19. Персонаж (character) → Дополнение (expansion)
**Тип связи**: Один-ко-многим  
У одного персонажа одно дополнение.  
У одного дополнения несколько персонажей.  
`character.expansion_id` → `expansion.id`

#### 20. Персонаж (character) → Локация (location)
**Тип связи**: Один-ко-многим  
У одного персонажа одна локация.  
У одной локации несколько персонажей.  
`character.location_id` → `location.id`

#### 21. Персонаж (character) → Профессии (profession) 
**Тип связи**: Многие-ко-многим (через `character_profession`)  
У одного персонажа 2 профессии.  
У одной профессии несколько персонажей.  
`character.id` → `character_profession.character_id`  
`profession.id` → `character_profession.profession_id`

#### 22. Персонаж (character) → Рецепт (recipe) 
**Тип связи**: Многие-ко-многим (через `character_recipe`)  
У одного персонажа несколько рецептов.  
У одного рецепта несколько персонажей.  
**Внешние ключи**:  
`character.id` → `character_recipe.character_id`  
`recipe.id` → `character_recipe.recipe_id`

#### 23. Рецепт (recipe) → Профессия (profession)
**Тип связи**: Один-ко-многим  
У одного рецепта одна профессия.  
У одной профессии несколько рецептов.  
**Внешние ключи**:  
`profession.id` → `recipe.profession_id`

#### 24. Персонаж (character) → Предмет (item) (Инвентарь)  
**Тип связи**: Один-ко-многим  
У одного персонажа несколько "инвентарных предметов".  
У одного "инвентарного предмета" один персонаж.  
**Внешний ключ**:  
`character.id` → `inventory_item.character_id`

#### 25. Персонаж (character) → Предмет (item) (Банк)
**Тип связи**: Один-ко-многим  
У одного персонажа несколько "банковских предметов".  
У одного "банковского предмета" один персонаж.  
**Внешний ключ**:  
`character.id` → `bank.character_id`

#### 26. Персонаж (character) → Предмет (item) (Экипировка)
**Тип связи**: Один-ко-многим (через `character_equipment`, ради слота - шея, голова, спина...)  
У одного персонажа несколько "предметов экипировки".  
У одного "предмета экипировки" один персонаж.  
**Внешний ключ**:  
`character.id` → `character_equipment.character_id`  
`item.id` → `character_equipment.item_id`

#### 27. Задание (quest) → Цели (objective)
**Тип связи**: Один-ко-многим  
У одного задания несколько целей.  
У одной цели одно задание.  
**Внешний ключ**:  
`quest.id` → `objective.quest_id`

#### 28. Персонаж (character) → Задания (quest)  
**Тип связи**: Многие-ко-многим (через `character_quest`)  
У одного персонажа несколько заданий.  
Одно задание берут несколько игроков.  
**Внешние ключи**:  
`character.id` → `character_quest.character_id`  
`quest.id` → `character_quest.quest_id`

#### 29. Задания персонажа (character_quest) → Цели (objective)
 **Тип связи**: Многие-ко-многим (через `character_quest_objectives`)  
У одного задания персонажа несколько целей.  
На одну цель могут ссылаться задания разных персонажей.  
**Внешние ключи**:  
`character_quest.id` → `character_quest_objectives. character_quest_id`  
`objective.id` → `character_quest_objectives.objective_id`

#### 30. Задание (quest) → Предметы (item) (Награда)                   
 **Тип связи**: Многие-ко-многим (через `quest_rewards`)  
У одного задания несколько наград.  
На одну награду могут ссылаться разные задания.  
**Внешние ключи**:  
`quest.id` → `quest_rewards.quest_id`  
`item.id` → `quest_rewards.item_id`

#### 31. Гильдия (guild) → Персонажи (character)
**Тип связи**: Один-ко-многим (через `guild_character` ради ранга)  
У одной гильдии несколько персонажей.  
У одного персонажа одна гильдия.  
**Внешние ключи**:  
`guild.id` → `guild_character.guild_id`  
`character.id` → `guild_character.character_id`

#### 32. Моб (mob) → Предмет (item) (Лут)
**Тип связи**: Многие-ко-многим (через `mob_loot`)  
У одного моба несколько предметов в луте.  
У одного предмета в луте несколько мобов с которого предмет может выпасть.  
**Внешние ключи**:  
`mob.id` → `mob_loot.mob_id`  
`item.id` → `mob_loot.item_id`

#### 33. Аккаунт (account) → История входов (login_history)
**Тип связи**: Один-ко-многим  
У одного аккаунта несколько записей.  
У одной записи один аккаунт.  
**Внешние ключи**:  
`account.id` → `login_history.account_id`

#### 34. Аккаунт (account) → История изменений (account_history)
**Тип связи**: Один-ко-многим  
У одного аккаунта несколько записей.  
У одной записи один аккаунт.  
**Внешние ключи**:  
`account.id` → `account_history.account_id`

лаба на авторизацию, пред и пост условий
#### 35. Аккаунт (account) → Аккаунт (account) (Друзья)
**Тип связи**: Многие-ко-многим (через `account_friend`)  
У одного аккаунта несколько записей.  
У одной записи один аккаунт.  
**Внешние ключи**:  
`account.id` → `account_friend.account_id`  
`account.id` → `account_friend.friend_id`

#### 36. Аккаунт (account) → Аккаунт (account) (Игнорируемые)
**Тип связи**: Многие-ко-многим (через `account_ignore`)  
У одного аккаунта несколько игнорируемых аккаунтов.  
У игнорируемого аккаунта может быть несколько игнорщиков.  
**Внешние ключи**:  
`account.id` → `account_ignore.account_id`  
`account.id` → `account_ignore.ignored_id`

#### 37. Раса (race) → Локация (location)  
**Тип связи**: Один-к-одному  
У одной расы одна стартовая локация.  
У одной стартовой локации одна раса.  
**Внешний ключ**:  
`location.id` → `race.starting_zone_id`

#### 38. Предмет (item) → Дополнение (expansion)
**Тип связи**: Один-ко-многим  
У одного предмета одно дополнение.  
У одного дополнения несколько предметов.  
**Внешний ключ**:  
`expansion.id` → `item.expansion_id`

#### 39. Проф предмет (item) → Профессия (profession)
**Тип связи**: Один-ко-многим  
У одного проф предмета одна профессия.  
У одной профессии несколько проф предметов.  
**Внешний ключ**:  
`profession.id` → `trade_goods.profession_id`

#### 40. Персонаж (character) → Сумка (bags) (Ячейка для предмет-сумки)
**Тип связи**: Один-ко-многим (через `bags` ради ссылки на предмет-сумку)  
У одного персонажа несколько сумок.  
У одной сумки один персонаж.  
**Внешний ключ**:  
`character.id` → `bags.character_id`  
`item.id` → `bags.item_id`

#### 41. Локация (location) → Дополнение (expansion)
**Тип связи**: Один-ко-многим  
У одной локации одно дополнение.  
У одного дополнения несколько локаций.  
**Внешний ключ**:  
`expansion.id` → `location.expansion_id`

#### 42. Рецепт (recipe) → Дополнение (expansion)
**Тип связи**: Один-ко-многим  
У одного рецепта одно дополнение.  
У одного дополнения несколько рецептов.  
**Внешний ключ**:  
`expansion.id` → `recipe.expansion_id`

#### 43. Рецепт (recipe) → Создаваемый предмет (item)
**Тип связи**: Один-к-одному  
У одного рецепта один создаваемый предмет.  
У одного создаваемый предмет один рецепт.  
**Внешний ключ**:  
`item.id` → `recipe.result_item_id`

#### 44. Рецепт (recipe) → Предмет (item) (Ингредиенты)
**Тип связи**: Многие-ко-многим  (через `recipe_ingredients`)  
У одного рецепта несколько игредиентов.  
У одного ингредиента несколько использующих его рецептов.  
**Внешний ключ**:  
`item.id` → `recipe_ingredients.item_id`  
`recipe.id` → `recipe_ingredients.recipe_id`

#### 45. Аккаунт (account) → Сообщество (community)
**Тип связи**: Многие-ко-многим (через `community_account`)  
У одного аккаунта несколько сообществ.  
У одного сообщества несколько вступивших в него аккаунтов.  
**Внешний ключ**:  
`account.id` → `community_account.account_id`  
`community.id` → `community_account.community_id`

#### 46. Подземелье (dungeon) → Локация (location)
**Тип связи**: Один-ко-многим  
У одного подземелья одна локация.  
У одной локации несколько поземелий.  
**Внешний ключ**:  
`location.id` → `dungeon.location_id`

#### 47. Подземелье (dungeon) → Дополнение (expansion)
**Тип связи**: Один-ко-многим  
У одного подземелья одно дополнение.  
У одного дополнения несколько подземелий.  
**Внешний ключ**:  
`expansion.id` → `dungeon.expansion_id`

#### 48. Рейд (raid) → Локация (location)
**Тип связи**: Один-ко-многим  
У одного рейда одно дополнение.  
У одного дополнения несколько рейдов.  
**Внешний ключ**:  
`location.id` → `raid.location_id`

#### 49. Рейд (raid) → Дополнение (expansion)
**Тип связи**: Один-ко-многим  
У одного рейда одно дополнение.  
У одного дополнения несколько рейдов.  
**Внешний ключ**:  
`expansion.id` → `raid.expansion_id`

#### 50. Моб (mob) → Локация (location)
**Тип связи**: Один-ко-многим  
У одного моба одна локация.  
У одной локации несколько мобов.  
**Внешний ключ**:  
`location.id` → `mob.location_id`

#### 51. Персонаж (character) → Валюта (currency)
**Тип связи**: Многие-ко-многим (через `character_currency`)  
У одного персонажа несколько валют.  
У одной валюты несколько персонажей.  
**Внешний ключ**:  
`character.id` → `character_currency.character_id`  
`currency.id` → `character_currency.currency_id`

#### 52. Персонаж (character) → Репутация (reputation)
**Тип связи**: Многие-ко-многим (через `character_reputation`)  
У одного персонажа несколько репутаций.  
У одной репутации несколько персонажей.  
**Внешний ключ**:  
`character.id` → `character_reputation.character_id`  
`reputation.id` → `character_reputation.faction_id`

#### 53. Аккаунт (account) → Транспорт (mount)
**Тип связи**: Многие-ко-многим (через `account_mount`)  
У одного аккаунта несколько транспортов.  
У одного транспорта несколько аккаунтов.  
**Внешний ключ**:  
`account.id` → `account_mount.account_id`  
`mount.id` → `account_mount.mount_id`

#### 54. Аккаунт (account) → Питомцы (pet)
**Тип связи**: Многие-ко-многим (через `account_pet`)  
У одного аккаунта несколько питомцев.  
У одного питомца несколько аккаунтов.  
**Внешний ключ**:  
`account.id` → `account_pet.account_id`  
`pet.id` → `account_pet.pet_id`

#### 55. Аккаунт (account) → Игрушки (toy)
**Тип связи**: Многие-ко-многим (через `account_toy`)  
У одного аккаунта несколько игрушек.  
У одной игрушки несколько аккаунтов.  
**Внешний ключ**:  
`account.id` → `account_toy.account_id`  
`toy.id` → `account_toy.toy_id`

#### 56. Аккаунт (account) → Звания (title)
**Тип связи**: Многие-ко-многим (через `account_title`)  
У одного аккаунта несколько званий.  
У однго звания несколько аккаунтов.  
**Внешний ключ**:  
`account.id` → `account_title.account_id`  
`title.id` → `account_title.title_id`

#### 57. Персонаж (character) → Персонаж (character) (Письмо)
**Тип связи**: Многие-ко-многим (через `writing`)  
У одного персонажа несколько писем (от других персонажей).  
**Внешние ключи**:  
`character.id` → `writing.sender_id`  
`character.id` → `writing.recipient_id`

#### 58. Письмо (writing) → Предметы (item)
**Тип связи**: Один-ко-многим  
У одного письма несколько вложенных предметов.  
У одного вложенного предмета одно письмо.  
**Внешний ключ**:  
`item.id` → `writing_items.item_id`

#### 59. Персонаж (character) → Предмет (item) (Аукцион)
**Тип связи**: Один-ко-многим  
У одного персонажа несколько аукционных лотов (предметов).  
У одного аукционного лота (предмета) один персонаж.  
**Внешний ключ**:  
`Character.id` → `auction_lot.character_id`

#### 60. Цель (objective) → Моб (mob)
**Тип связи**: Один-к-одному  
У одной цели один моб.  
Один моба используется в одной цели.  
**Внешний ключ**:  
`mob.id` → `objective.target_mob_id`

#### 61. Цель (objective) → Предмет (item)
**Тип связи**: Один-к-одному  
У одной цели один предмет.  
У одного предмета одна цель.  
**Внешний ключ**:  
`item.id` → `objective.target_item_id`

---
### ER Диаграмма

Сайт с удобным интерфейсом для просмотра диаграммы
https://dbdiagram.io/d/World-of-Warcraft-67fadf714f7afba1845eca7c

### Соответсвие 3НФ

### Соответствие модели третьей нормальной форме (3НФ)

**Модель базы данных полностью соответствует требованиям третьей нормальной формы (3НФ).**  
**Обоснование:**

#### 1. **Выполнение требований 1НФ и 2НФ:**
- **Атомарность данных**: Все поля в таблицах содержат атомарные значения (например, `character.name` — строка, `gender` — ENUM). Отсутствуют массивы, списки или JSON-поля, нарушающие атомарность.
- **Полная зависимость от первичного ключа**:  
  - В таблицах с составными ключами (например, `character_currency`, `recipe_ingredients`) неключевые атрибуты зависят от всего ключа. Например, `amount` в `character_currency` зависит от пары `(character_id, currency_id)`.  
  - В таблицах с простыми ключами (например, `account`, `item`) все неключевые поля зависят только от первичного ключа.

#### 2. **Отсутствие транзитивных зависимостей:**
- **Использование внешних ключей**: Вместо хранения данных напрямую (например, названия сервера в `character`) используются ссылки на ID (`server_id`), что исключает зависимость от неключевых атрибутов других таблиц.  
- **Разделение сущностей**:  
  - Свойства предметов (например, урон оружия, прочность брони) вынесены в отдельные таблицы (`weapon`, `armor`), что устраняет зависимость от поля `item_class` в таблице `item`.  
  - Статы (характеристики) предметов хранятся в `item_stats`, где значения зависят только от комбинации `(item_id, stat_type)`.

#### 3. **Нормализация составных данных:**
- **Отсутствие избыточности**:  
  - Нет дублирования данных. Например, информация о профессиях хранится в таблице `profession`, а связь с персонажами — в `character_profession`.  
  - Многозначные поля (например, списки друзей, игнорируемых) реализованы через связующие таблицы (`account_friend`, `account_ignore`), что соответствует 3НФ.  
- **ENUM и внешние ключи**: Категоризация (например, `slot_type`, `quality`) реализована через ENUM и ссылки, а не через текстовые поля, что минимизирует избыточность.

#### 4. **Проверка на исключения:**
- **Таблица `item` и наследование**:  
  Несмотря на использование наследования (CTI), каждая дочерняя таблица (`weapon`, `armor`) имеет строгую связь с `item.id`, а триггеры гарантируют целостность (например, проверка `item_class`). Это не нарушает 3НФ, так как зависимости остаются в рамках первичных ключей.  
- **Поля с ENUM**:  
  ENUM-типы (например, `role` в `specialization`) не создают транзитивных зависимостей, так как их значения жестко заданы и не ссылаются на другие атрибуты.

#### 5. **Примеры соответствия:**
- **Таблица `character`**:  
  Поля `server_id`, `expansion_id`, `location_id` ссылаются на внешние ключи, а не хранят текстовые названия. Это исключает зависимость от неключевых данных других таблиц.  
- **Таблица `character_quest`**:  
  Поле `status` зависит только от первичного ключа `id`, а не от других атрибутов, таких как `quest_id` или `character_id`.  

#### Итог:
Модель удовлетворяет всем критериям 3НФ:  
1. Все таблицы соответствуют 1НФ и 2НФ.  
2. Нет транзитивных зависимостей — неключевые атрибуты зависят **только от первичного ключа**.  
3. Данные нормализованы, отсутствует избыточность и дублирование.  
4. Связи между сущностями реализованы через внешние ключи, что обеспечивает целостность и минимизирует аномалии при модификации данных.