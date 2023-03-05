import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# Connect to the MongoDB instance using Motors
client = AsyncIOMotorClient('mongodb://localhost:27017/')

# Select the database and collection
db = client['shopify-database']
collection = db['applications']

# Define an async function to insert a document
async def insert_document(document):
    # Check if the document already exists in the collection
    if await collection.count_documents(document) == 0:
        # If the document does not exist, insert it
        result = await collection.insert_one(document)
        print(f"Inserted document with _id: {result.inserted_id}")
    else:
        # If the document already exists, print a message indicating this
        print("Document already exists in collection.")

# Define the documents to be inserted
documents = [
    {"username": "user1", "email": "user1@example.com"},
    {"username": "user2", "email": "user2@example.com"},
    {"username": "user3", "email": "user3@example.com"},
    {"username": "user1", "email": "user1@example.com"},  # duplicate
]

# Insert each document asynchronously using the insert_document() function
loop = asyncio.get_event_loop()
tasks = [insert_document(document) for document in documents]
loop.run_until_complete(asyncio.gather(*tasks))

# Print a message indicating that all documents have been inserted
print("All documents have been inserted.")
