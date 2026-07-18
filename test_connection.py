from database.db import resume_collection

resume_collection.insert_one({
    "status": "MongoDB Connected"
})

print("MongoDB Connected Successfully")