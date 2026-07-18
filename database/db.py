from pymongo import MongoClient

MONGO_URI = "mongodb+srv://Reshrms:asdfghjkl@cluster0.gfkogrq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)


db = client["Resume_Project"]


resume_collection = db["resumes"]