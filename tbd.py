from pymongo import MongoClient
import certifi

#Replace <db_username> and <db_password> with your actual username and password
#client = MongoClient("mongodb+srv://user:BUiIZW9wSnqgPbhN@histcluster.lijlj.mongodb.net/personaDB?retryWrites=true&w=majority", tlsCAFile=certifi.where())
client = MongoClient("mongodb+srv://arunsridhar78:t4SSnBrmusRe5Pst@agentic.3thxi.mongodb.net/?retryWrites=true&w=majority&appName=agentic", tlsCAFile=certifi.where())

#Specify database and collection
db = client["sample_training"]
mycol = db["routes"]
myquery= {"src_airport":"CEK"} #{"name": "Benjamin Netanyahu"}
document = list(mycol.find(myquery))
for d in document:
    op=d['airline']
    print(f"id: {op['id']}")
    print(f"name: {op['name']}")
    # print(f"id: ",d['id'])
    # print(f"name: {d['name']}")
    # print(f"alias: {d['alias']}")
    # print(f"iata: {d['iata']}")
    # print(f"src_airport: {d['src_airport']}")
    # print(f"dst_airport: {d['dst_airport']}")
    # print(f"codeshare: {d['codeshare']}")
    # print(f"stops: {d['stops']}")
    # print(f"airplane: {d['airplane']}")



#figures = document['routes']
#print(document)


#{'id': 410, 'name': 'Aerocondor', 'alias': '2B', 'iata': 'ARD'}, 'src_airport': 'CEK', 'dst_airport': 'KZN', 'codeshare': '', 'stops': 0, 'airplane': 'CR2'}