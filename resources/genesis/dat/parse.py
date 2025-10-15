import xml.etree.ElementTree as ET
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table

# Database setup using SQLAlchemy
engine = create_engine('sqlite:///roms.db')
metadata = MetaData()
metadata.create_all(engine)

# Define the database table schema
games_table = Table('games', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('description', String),
)
roms_table = Table('roms', metadata,
    Column('id', Integer, primary_key=True),
    Column('game_id', Integer),
    Column('name', String),
    Column('size', Integer),
    Column('crc', String),
    Column('md5', String),
    Column('sha1', String),
)

metadata.create_all(engine)

# Parse the XML file
tree = ET.parse('gen_roms.dat.xml')
root = tree.getroot()
games_to_insert = []
roms_to_insert = []
game_id_counter = 1

for game in root.findall('game'):
    game_name = game.get('name')
    description = game.find('description').text if game.find('description') is not None else None

    # Gather data for the 'games' table
    games_to_insert.append({
        'id': game_id_counter,
        'name': game_name,
        'description': description
    })

    # Gather data for the 'roms' table
    for rom in game.findall('rom'):
        roms_to_insert.append({
            'game_id': game_id_counter,
            'name': rom.get('name'),
            'size': int(rom.get('size')),
            'crc': rom.get('crc'),
            'md5': rom.get('md5'),
            'sha1': rom.get('sha1'),
        })
    
    game_id_counter += 1

# Insert the data into the database
with engine.connect() as connection:
    connection.execute(games_table.insert(), games_to_insert)
    connection.execute(roms_table.insert(), roms_to_insert)
    connection.commit()

print("Data parsed and inserted into roms.db successfully.")

