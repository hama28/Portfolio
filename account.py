from datetime import datetime
from http import client
from google.cloud import datastore

def insert(name, pw):
    client = datastore.Client()
    key = client.key("Account")
    entity = datastore.Entity(key=key)
    entity["name"] = name
    entity["pw"] = pw
    entity["created"] = datetime.now()
    client.put(entity)
    entity['id'] = entity.key.id
    return entity

def get_all():
    client = datastore.Client()
    query = client.query(kind='Account')
    data = list(query.fetch())
    for entity in data:
        entity['id'] = entity.key.id
    return data
