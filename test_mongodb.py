
from pymongo.mongo_client import MongoClient



uri = "mongodb+srv://stylesajwwf_db_user:X3pNJTwtvdI4rych@networksecuritycluster.ztlvx0e.mongodb.net/?appName=NetworkSecurityCluster"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)