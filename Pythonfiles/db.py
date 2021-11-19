def get_database():
    from pymongo import MongoClient
    import pymongo
    """ DB = "users"
    USERNAME = ""
    PASSWORD = ""
    HOST = "localhost"
    PORT = 27017

    MONGO_URI = 'mongodb://{host}:{port}/{database}'.format(
        username=USERNAME,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        database=DB
    ) """
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://172.26.14.137:27017"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING) 
    print(client)
    # Create the database for our example (we will use the same database throughout the tutorial
    return client['users']
    
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":    
    
    # Get the database
    dbname = get_database()
    print(dbname)