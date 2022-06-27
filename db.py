import pandas as pd
from model import Pathways, PositionEntry, Pathway
import util

filename = 'user_position.csv'
schema = ['id','position','start','end']

def read_csv(filename, schema) -> pd.DataFrame:
    df = pd.read_csv(filename)
    df.columns = schema

    return df

def parse_row(row) -> PositionEntry:
    start = row['start']
    end = row['end']

    days = util.time_between(start,end)

    return PositionEntry(row['id'], row['position'], days)

def parse_db(db) -> list:
    entries = []

    for _, row in db.iterrows():
        entries.append(parse_row(row))
    
    return entries

def to_users(db) -> dict:
    users = {}

    for entry in db:
        if entry.id not in users:
            users[entry.id] = [entry]
        else:
            users[entry.id].append(entry)

    return users

def generate_pathways(users) -> dict:
    pathways = {}

    for user in users.values():
        length = len(user)
        for index, entry in enumerate(user):
            if entry.position not in pathways:
                pathways[entry.position] = Pathway(entry.position, entry.days)
            else:
                pathways[entry.position].increment()

            next = index + 1

            if next < length:
                pathways[entry.position].add_path(user[next].position)

    for pathway in pathways.values():
        pathway.update_avg()

    return pathways

def fetch_pathways() -> Pathways:
    db = parse_db(read_csv(filename, schema))
    users = to_users(db)
    pathways = generate_pathways(users)

    return Pathways(pathways)