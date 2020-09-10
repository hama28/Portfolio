from datetime import datetime
from http import client
# from google.cloud import datastore

# データの追加
def insert(things, check):
    client = datastore.Client()
    key = client.key("TodoList")
    entity = datastore.Entity(key=key)
    entity["things"] = things
    entity["check"] = check
    entity["created"] = datetime.now()
    client.put(entity)
    entity['id'] = entity.key.id
    return entity

# データの取得
def get_all():
    client = datastore.Client()
    query = client.query(kind='TodoList')
    query.order = '-created'
    data = list(query.fetch())
    for entity in data:
        entity['id'] = entity.key.id
    return data

# 指定データの取得
def get_by_id(key_id):
    client = datastore.Client()
    key = client.key('Greeting', int(key_id))
    entity = client.get(key=key)
    if entity:
        entity['id'] = entity.key.id
    return entity

# データの更新
def update(entity):
    if 'id' in entity:
        del entity['id']
    client = datastore.Client()
    client.put(entity)
    entity['id'] = entity.key.id
    return entity

# データの削除
def delete(key_id):
    client = datastore.Client()
    key = client.key('Greeting', int(key_id))
    client.delete(key)


# エンティティグループ
# データの追加
def insert_comment(parent_id, message):
    client = datastore.Client()
    parent_key = client.key('Greeting', int(parent_id))
    key = client.key('Comment', parent=parent_key)
    entity = datastore.Entity(key=key)
    entity['message'] = message
    entity["created"] = datetime.now()
    client.put(entity)
    entity['id'] = entity.key.id
    return entity

# 子エンティティの取得
def get_comments(parent_id):
    client = datastore.Client()
    ancestor = client.key('Greeting', int(parent_id))
    query = client.query(kind='Comment', ancestor=ancestor)
    entities = list(query.fetch())
    for entity in entities:
        entity['id'] = entity.key.id
    return entities