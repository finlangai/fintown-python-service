from pymongo import MongoClient, errors

from dotenv import load_dotenv
import os

load_dotenv()


def get_database():
    try:
        client = MongoClient(os.getenv("MONGODB_URI"))
        return client[os.getenv("MONGODB_DB_NAME")]
    except errors.PyMongoError as e:
        print(f"Error connecting to database: {e}")
        return None


def get_collection(collection_name: str):
    db = get_database()
    if db is None:
        return None
    try:
        return db[collection_name]
    except errors.PyMongoError as e:
        print(f"Error getting collection '{collection_name}': {e}")
        return None


# ================
# =====INSERT=====
# ================
def insert_one(collection_name: str, document: dict):
    collection = get_collection(collection_name)
    if collection is None:
        return None
    try:
        result = collection.insert_one(document)
        return result.inserted_id
    except errors.PyMongoError as e:
        print(f"Error inserting document: {e}")
        return None


def insert_many(collection_name: str, documents: list):
    collection = get_collection(collection_name)
    if collection is None:
        return None
    try:
        result = collection.insert_many(documents)
        return result.inserted_ids
    except errors.PyMongoError as e:
        print(f"Error inserting documents: {e}")
        return None


# =================
# ======QUERY======
# =================
def find_one(collection_name: str, query: dict):
    collection = get_collection(collection_name)
    if collection is None:
        return None
    try:
        return collection.find_one(query)
    except errors.PyMongoError as e:
        print(f"Error finding document: {e}")
        return None


def find_many(collection_name: str, query: dict):
    collection = get_collection(collection_name)
    if collection is None:
        return None
    try:
        return list(collection.find(query))
    except errors.PyMongoError as e:
        print(f"Error finding documents: {e}")
        return None


def query_with_projection(collection_name: str, query: dict, projection: dict):
    collection = get_collection(collection_name)
    if collection is None:
        return None
    try:
        return list(collection.find(query, projection))
    except errors.PyMongoError as e:
        print(f"Error finding documents: {e}")
        return None


# ================
# =====UPDATE=====
# ================
def update_one(collection_name: str, query: dict, update: dict):
    collection = get_collection(collection_name)
    if collection is None:
        return None
    try:
        result = collection.update_one(query, {"$set": update})
        return result.modified_count
    except errors.PyMongoError as e:
        print(f"Error updating document: {e}")
        return None


def update_many(collection_name: str, query: dict, update: dict):
    collection = get_collection(collection_name)
    if collection is None:
        return None
    try:
        result = collection.update_many(query, {"$set": update})
        return result.modified_count
    except errors.PyMongoError as e:
        print(f"Error updating documents: {e}")
        return None


# ================
# =====DELETE=====
# ================
def delete_one(collection_name: str, query: dict):
    collection = get_collection(collection_name)
    if collection is None:
        return None
    try:
        result = collection.delete_one(query)
        return result.deleted_count
    except errors.PyMongoError as e:
        print(f"Error deleting document: {e}")
        return None


def delete_many(collection_name: str, query: dict):
    collection = get_collection(collection_name)
    if collection is None:
        return None
    try:
        result = collection.delete_many(query)
        return result.deleted_count
    except errors.PyMongoError as e:
        print(f"Error deleting documents: {e}")
        return None
