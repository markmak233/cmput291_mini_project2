# load the necessary libary
from pymongo import MongoClient
import json,time
import sys
# open library
def loadDB(db,json_name,collname):
    # drop if table exist
    list_of_collections = db.list_collection_names()
    if json_name in list_of_collections:
        db[collname].drop()
    # connect to a collection
    collection=db[collname]
    try:
        with open(json_name) as file:
            file_data = json.load(file)
    except:
        print("json file does not exist")
        return
    # import instence
    if isinstance(file_data, list):
        collection.insert_many(file_data)
    else:
        collection.insert_one(file_data)
    print("{} loaded".format(json_name))
        
        
# user input
# if typed python3 tsv-2-json.py 27017(defult)
# it will us: python3 transfer_off.py 27017 name.basics.json title.basics.json title.principals.json title.ratings.json
# otherwise it will load user requestd file
if __name__ == "__main__":
    st=time.time()
    # no port information
    if len(sys.argv) == 1:
        print("Mongo DB port information required")
    # loading defult sitaction
    elif len(sys.argv) == 2:
        print(" load json:\n name.basics.json \n title.basics.json\n title.principals.json\n title.ratings.json ")
        list_of_file=['name.basics.json','title.basics.json','title.principals.json','title.ratings.json']
    else:
        print(" too many arguments")
    
    # only do when all information meet
    if len(sys.argv) == 2:
        print('-'*12)
        db=None
        # connect database
        try:
            location='mongodb://localhost:'+str(int(sys.argv[1]))
            client = MongoClient(location)
            db=client["291db"]
        except:
            print("fail to connect mongoDB server")
        if db!=None:
            # load each collection
            for i in range(len(list_of_file)):
                collname=list_of_file[i].split('.')
                collname=collname[0]+'_'+collname[1]
                loadDB(db,list_of_file[i],collname)
        print("programme end in {} seconds.".format(int(time.time()-st)))