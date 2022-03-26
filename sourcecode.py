from pymongo import MongoClient
import sys,os

def search_title(db):
    collection = db['title_basis']
    collection.find('xxxxx')
    input('1')


def search_genres(db):
    input('2')


def search_caster(db):
    input('3')


def add_movie(db):
    input('4')


def add_castre(db):
    input('5')



def main():
    db=None
    try:
        location='mongodb://localhost:'+str(int(sys.argv[1]))
        client = MongoClient(location)
        db=client["291db"]
    except Exception as e:
        print("fail to connect ",location)
    while db is not None:
        print('''
        1.Search for titles 
        2.Search for genres
        3.Search for cast/crew members
        4.Add a movie
        5.Add a cast/crew member
        5.exit\n
        ''')
        sel=input('> ')
        if sel not in ['1','2','3','4','5','6']:
            print('unidentify input')
        elif sel == '1':
            search_title(db)
        elif sel == '2':
            search_genres(db)
        elif sel == '3':
            search_caster(db)
        elif sel == '4':
            add_movie(db)
        elif sel == '5':
            add_castre(db)
        elif sel == '6':
            db = None

if "__name__" == "__main__":
    if len(sys.argv)!=2:
        print("ex. Python3 sourcecide 27017")
    else:
        main()