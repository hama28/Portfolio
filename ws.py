import requests
from bs4 import BeautifulSoup
from datetime import datetime
from http import client
from google.cloud import datastore


# スクレイピング
def get_hatebu(users):
    hatebu_array = []

    r = requests.get('http://b.hatena.ne.jp/')
    content = r.content
    soup = BeautifulSoup(content, 'html.parser')

    for div in soup.select("div.entrylist-contents-main"):
        title = div.h3
        user = div.span
        user_num = user.getText().split(" ")
        keisai = div.p
        url = div.a

        if int(user_num[0]) >= int(users):
            data_list = []
            data_list.append(title.getText())
            data_list.append(user_num[0])
            data_list.append(keisai.getText())
            data_list.append(url.get('href'))
            hatebu_array.append(data_list)
        else:
            next

    return hatebu_array

# 親データ追加
def insert(target, users):
    client = datastore.Client()
    key = client.key("ScrapingDataSummary")
    entity = datastore.Entity(key=key)
    entity["target"] = target
    entity["over_num"] = users
    entity["created"] = datetime.now()
    client.put(entity)
    entity['id'] = entity.key.id
    # 追加した親データのkey_idを返す
    return entity.key.id

# 子データ追加
def insert_descendant(parent_id, web_array):
    for web in web_array:
        client = datastore.Client()
        parent_key = client.key('ScrapingDataSummary', int(parent_id))
        key = client.key('ScrapingDataDetails', parent=parent_key)
        entity = datastore.Entity(key=key)
        entity['title'] = web[0]
        entity['users'] = web[1]
        entity['web_name'] = web[2]
        entity['url'] = web[3]
        client.put(entity)
    return entity

# 親データ一覧の取得
def get_all():
    client = datastore.Client()
    query = client.query(kind='ScrapingDataSummary')
    query.order = '-created'
    data = list(query.fetch())
    for entity in data:
        entity['id'] = entity.key.id
    return data

# 選択された親データに紐付く子データ一覧の取得
def get_data(parent_id):
    client = datastore.Client()
    ancestor = client.key('ScrapingDataSummary', int(parent_id))
    query = client.query(kind='ScrapingDataDetails', ancestor=ancestor)
    entities = list(query.fetch())
    for entity in entities:
        entity['id'] = entity.key.id
    return entities