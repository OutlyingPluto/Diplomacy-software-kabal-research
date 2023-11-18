import sqlite3

# connect database with sqlite3
def getConnection(db):
    connection = sqlite3.connect(db, check_same_thread=False)
    return connection

diplo_db = getConnection("diplomacy.db")

# execute a write query into database
def executeWriteQuery(connection, query, placeholders=()):
    cursor = connection.cursor()
    print(query, placeholders)
    cursor.execute(query, placeholders)
    connection.commit()
    return True


# execute a read query from database
def executeReadQuery(connection, query, placeholders=()):
    cursor = connection.cursor()
    print(query, placeholders)
    cursor.execute(query, placeholders)
    return cursor.fetchall()

event_table_maker = """
CREATE TABLE IF NOT EXISTS events (
    eID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name varchar(1000),
    datetime TEXT,
    subclass varchar(255),
    country_of_origin varchar(127),
    local_risk INTEGER
);
"""
# eID | name | datetime (time frame when the event happened) | subclass (political, religious, cultural etc.)


country_table_maker = """
CREATE TABLE IF NOT EXISTS countries (
    cID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name varchar(127),
    regime_type varchar(31),
    political_stability_index INTEGER,
    economic_stability_index INTEGER
);
"""
# cID | name | regime_type (monarchy/democracy/republic etc.) | political_stability_index (how prone it is to political collapse) | economic_stability_index (how prone it is to economic collapse)
# for stability index, higher number means more stable


event_to_country_table_maker = """
CREATE TABLE impacts (
    event_id INTEGER REFERENCES events(eID),
    countryA_id INTEGER REFERENCES countries(cID),
    countryB_id INTEGER REFERENCES countries(cID),
    risk_political INTEGER,
    risk_economic INTEGER
);
"""
# event_id | country1 (first country affected) | country2 (second country affected) | impact (impact on relationship between the two countries)
# for impact, positive number means relationship is worsened, negative number means relationship is bettered, 0 means no/negligible impact

custom_query = """

"""

executeWriteQuery(diplo_db, event_to_country_table_maker)