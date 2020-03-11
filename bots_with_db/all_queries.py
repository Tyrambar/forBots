
DEFAULT_ATTRS_EVENT = ['name', 'address', 'date', 'description', 'host_id']
DEFAULT_ATTRS_EVENT_VK = DEFAULT_ATTRS_EVENT + ['vk_host_id']
DEFAULT_ATTRS_EVENT_TG = DEFAULT_ATTRS_EVENT + ['tg_host_id']

# First queries for creating tables
create_users = """
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  vk_id INTEGER NOT NULL, 
  tg_id INTEGER NOT NULL,
  passw CHAR(10) NOT NULL
)
"""
create_events = """
CREATE TABLE IF NOT EXISTS events (
  id SERIAL PRIMARY KEY,
  name VARCHAR(40) NOT NULL UNIQUE,
  address VARCHAR(100) NOT NULL, 
  date TIMESTAMP NOT NULL,
  description TEXT NOT NULL,
  host_id INTEGER REFERENCES users(id)
)
"""
create_signs = """
CREATE TABLE IF NOT EXISTS signs (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON UPDATE CASCADE, 
  event_id INTEGER REFERENCES events(id) ON DELETE CASCADE
)
"""

EVENTS_LIST = """SELECT name FROM events ORDER BY date"""
ADD_EVENT = """INSERT INTO events (name, address, date, description, host_id)
                        VALUES (%s, %s, %s, %s, %s)"""
DEL_EVENT = """DELETE FROM events WHERE name = %s"""
EDIT_EVENT = f"""UPDATE events SET {' = %s, '.join(DEFAULT_ATTRS_EVENT)} = %s
                        WHERE name = %s """
GET_EVENT_ALL = f"""SELECT {', '.join(DEFAULT_ATTRS_EVENT[:-1])}, us.vk_id, us.tg_id FROM events ev
                    INNER JOIN users us ON ev.host_id = us.id WHERE ev.name = %s """
GET_ID_EVENT_BY_NAME = """SELECT id FROM events WHERE name = %s"""
GET_HOST_ID_ALL = """SELECT us.vk_id, us.tg_id FROM users us
                        INNER JOIN events ev ON us.id = ev.host_id 
                           WHERE ev.name = %s"""

ADD_USER_T = """INSERT INTO users (vk_id, tg_id, passw)
                        VALUES (%s, %s, %s)"""
GET_ID_USER_BY_VK = """SELECT id FROM users WHERE vk_id = %s"""
GET_ID_USER_TG_VK = """SELECT id FROM users WHERE tg_id = %s"""


ALL_PASSW = """SELECT passw FROM users"""
ALL_VK_ID = """SELECT vk_id FROM users"""
ALL_TG_ID = """SELECT tg_id FROM users"""
DEL_USER_VK = """DELETE FROM users WHERE vk_id = %s"""
DEL_USER_TG = """DELETE FROM users WHERE tg_id = %s"""
SYNC_DB_WITH_TG = """UPDATE users SET vk_id = %s
                        WHERE passw = %s """
SYNC_DB_WITH_VK = """UPDATE users SET tg_id = %s
                        WHERE passw = %s """
GET_PASSW_BY_VK = """SELECT passw FROM users WHERE vk_id = %s """
GET_PASSW_BY_TG = """SELECT passw FROM users WHERE tg_id = %s """


ALL_SIGNED_ID = """SELECT user_id FROM signs"""
ALL_SIGNED_ID_BY_EV_ALL = """SELECT us.vk_id, us.tg_id FROM users us 
                            INNER JOIN signs si ON us.id = si.user_id 
                                INNER JOIN events ev ON si.event_id = ev.id 
                                    WHERE us.id = si.user_id AND ev.name = %s"""
GET_SIGNS_BY_ID = """SELECT si.user_id FROM signs si
            INNER JOIN events ev ON si.event_id = ev.id WHERE si.user_id = %s AND ev.name = %s"""
ADD_SIGNS = """INSERT INTO signs (user_id, event_id) VALUES (%s, %s)"""
DEL_SIGNS = """DELETE FROM signs WHERE user_id = %s and event_id = %s"""


