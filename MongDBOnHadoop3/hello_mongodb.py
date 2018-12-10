#!/usr/bin/python3

#本文代码来自https://api.mongodb.com/python/current/tutorial.html

import pymongo

from pymongo import MongoClient
client = MongoClient()
client = MongoClient('localhost', 27017)

#client = MongoClient('mongodb://localhost:27017/')

#db = client.test_database

db = client['xgm-database']

#A collection is a group of documents stored in MongoDB ≈ a table in a relational database.
#collection = db.test_collection

collection = db['xgm-collection']

#以上操作没有创建数据，只有真正插入数据，才会创建。
#Collections and databases are created when the first document is inserted into them.

import datetime
post = {"author": "Mike",
          "text": "My first blog post!",
          "tags": ["mongodb", "python", "pymongo"],
          "date": datetime.datetime.utcnow()
          }

posts = db.posts
post_id = posts.insert_one(post).inserted_id
#insert_one()返回InsertOneResult对象
print (post_id)
#输出
#ObjectId('...')


#执行了上述的插入操作之后，posts就成了一个collection，通过如下查看所有collections
db.collection_names(include_system_collections=False)

import pprint
#返回第一个document
pprint.pprint(posts.find_one())

#限定查询
pprint.pprint(posts.find_one({"author": "Mike"}))

#返回：
#{u'_id': ObjectId('...'),
# u'author': u'Mike',
# u'date': datetime.datetime(...),
# u'tags': [u'mongodb', u'python', u'pymongo'],
# u'text': u'My first blog post!'}


posts.find_one({"author": "Eliot"})
#none

#我们可以通过ObjectId查询
pprint.pprint(posts.find_one({"_id": post_id}))

#ObjectId不同于string，以下查询没有结果
post_id_as_str = str(post_id)
posts.find_one({"_id": post_id_as_str}) # No result


from bson.objectid import ObjectId

# The web framework gets post_id from the URL and passes it as a string
def get(post_id):
    # Convert from string to ObjectId:
     document = client.db.collection.find_one({'_id': ObjectId(post_id)})

#批量插入
new_posts = [{"author": "Mike",
               "text": "Another post!",
               "tags": ["bulk", "insert"],
               "date": datetime.datetime(2018, 11, 12, 11, 14)
               },
              {"author": "Eliot",
               "title": "MongoDB is fun",
               "text": "and pretty easy too!",
               "date": datetime.datetime(2018, 11, 10, 10, 45)
               }
               ]

#The result from insert_many() now returns two ObjectId instances, one for each inserted document.               
result = posts.insert_many(new_posts)
print (result.inserted_ids)


#Querying for More Than One Document
# find() returns a Cursor instance，we can iterate
for post in posts.find():
     pprint.pprint(post)

for post in posts.find({"author": "Mike"}):
     pprint.pprint(post)


print (posts.count_documents({}))

print (posts.count_documents({"author": "Mike"}))


#Range Queries
#将结果按照键值排序
d = datetime.datetime(2017, 11, 12, 12)
for post in posts.find({"date": {"$lt": d}}).sort("author"):
     pprint.pprint(post)


#Indexing
result = db.profiles.create_index([('user_id', pymongo.ASCENDING)],unique=True)
print ("Indexing")
print (sorted(list(db.profiles.index_information())))

user_profiles = [
     {'user_id': 211, 'name': 'Luke'},
     {'user_id': 212, 'name': 'Ziltoid'}
     ]

result = db.profiles.insert_many(user_profiles)

new_profile = {'user_id': 213, 'name': 'Drew'}
duplicate_profile = {'user_id': 212, 'name': 'Tommy'}
result = db.profiles.insert_one(new_profile)  # This is fine.


#这里会报错，因为user_id重复了。
from pymongo.errors import DuplicateKeyError
try:
     result = db.profiles.insert_one(duplicate_profile)
except DuplicateKeyError as err:
     print ("DuplicateKeyError err!!" , err)
