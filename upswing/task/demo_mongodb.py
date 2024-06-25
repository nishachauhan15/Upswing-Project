from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')


# Access a specific database
db = client['test']

# Access a collection within the database
collection = db['mycollection']

# Insert a document into the collection
document = {"name": "John", "age": 30}
result = collection.insert_one(document)
print(f"Inserted document with id: {result.inserted_id}")


# Find documents in the collection
for doc in collection.find({"age": {"$gte": 25}}):
    print(doc)



# Update a document in the collection
query = {"name": "John"}
new_values = {"$set": {"age": 32}}
result = collection.update_one(query, new_values)
print(f"Modified {result.modified_count} document(s)")


# Delete a document from the collection
# query = {"name": "John"}
# result = collection.delete_one(query)
# print(f"Deleted {result.deleted_count} document(s)")
