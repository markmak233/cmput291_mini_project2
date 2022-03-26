from pymongo import MongoClient
import json,time
import sys

def p2q2(db):
    collection = db['title_basics']
    # create instence

    qurry=[
    {
        '$match': {
            'genres': {
                '$regex': 'drama', 
                '$options': 'i'
            }
        }
    }, {
        '$lookup': {
            'from': 'title_ratings', 
            'localField': 'tconst', 
            'foreignField': 'tconst', 
            'as': 'rating'
        }
    }, {
        '$unwind': {
            'path': '$rating'
        }
    }, {
        '$project': {
            '_id': '$_id', 
            'primaryTitle': '$primaryTitle', 
            'genres': '$genres', 
            'averagRating': {
                '$toDecimal': '$rating.averageRating'
            }, 
            'numVotes': {
                '$toInt': '$rating.numVotes'
            }
        }
    }, {
        '$unwind': {
            'path': '$numVotes'
        }
    }, {
        '$match': {
            'numVotes': {
                '$gte': 200000
            }
        }
    }, {
        '$sort': {
            'averagRating': -1
        }
    }
]
    a=time.time()
    result=list(collection.aggregate(qurry,allowDiskUse=True))
    print(time.time() - a)
    for line in result:
        print(line) 
    if len(result) == 0:
        print('No results return')
    else:
        datadisplay(result)
    return


def datadisplay(result):
    # get the tittle of the result
    a=list(result[0].keys())
    a.remove('_id')


    current_pg=0
    per_page=5
    max_pg=int(len(a)/5)+1
    user_selection=None

    while user_selection!= '3':
        string=''
        for i in range(len(a)):
            if a[i] in ['primaryTitle','genres']:
                string=string+'{:<24} '.format(str(a[i]))
            else:
                string=string+'{:<12} '.format(str(a[i]))
        print(string)


        start=per_page*current_pg
        end=per_page*(current_pg+1)
        if end>len(result):
            end=len(result)

        for index in range(start,end):
            string=''
            for i in range(len(a)):
                substring=''
                if a[i]=='genres':
                    for x in range(len(result[index][a[i]])):
                        substring+=str(result[index][a[i]][x])+' '
                else:
                    substring+=str(result[index][a[i]])+' '
                
                if a[i] in ['primaryTitle','genres']:
                    if len(substring)<24:
                        string=string+'{:<24} '.format(str(substring))
                    else:
                        string=string+'{:<22}.. '.format(str(substring[:22]))
                else:
                    if len(substring)<12:
                        string=string+'{:<12} '.format(str(substring))
                    else:
                        string=string+'{:<10}.. '.format(str(substring[:10]))

            print(string)

        print('\n1:nextpage\n2:last page\n3:go back')
        user_selection=input('> ')
        if user_selection not in ['1','2','3']:
            print('unidentified')
        elif user_selection=='1' and current_pg<max_pg:
            current_pg+=1
        elif user_selection=='2' and current_pg>=1:
            current_pg-=1





if __name__ == '__main__':
    location='mongodb://localhost:27017'
    client = MongoClient(location)
    db=client["291db"]
    p2q2(db)