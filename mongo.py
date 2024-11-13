from pymongo import MongoClient
import certifi

#Replace <db_username> and <db_password> with your actual username and password
client = MongoClient("mongodb+srv://user:BUiIZW9wSnqgPbhN@histcluster.lijlj.mongodb.net/personaDB?retryWrites=true&w=majority", tlsCAFile=certifi.where())

#Specify database and collection
db = client["personaDB"]
collection = db["Personas"]

#Test the connection by retrieving one document
try:
    document = collection.find_one()
    if document:
        print("Connection successful! Retrieved document:", document)
        figures = document['historicalFigures']

        for figure in figures:
            print(f"id: {figure['id']}")
            print(f"name: {figure['name']}")
            print(f"period: {figure['period']}")
            print(f"facts: {', '.join(figure['facts'])}")
            print(f"hints: {', '.join(figure['hints'])}")
            print(f"image: {figure['image']}")
            print("\n" + "-" * 40 + "\n")
    else:
        print("Connection successful, but no documents found in the collection.")
except Exception as e:
    print("Connection failed:", e)
