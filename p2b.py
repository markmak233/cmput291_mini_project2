from pymongo import MongoClient
import json,time
import sys,os

def p2q2(db):
    # set up user input 
    user_sel=None
    user_input=['','0']
    submited=False
    valid_input1=list(range(ord('a'),ord('z')))+list(range(ord('A'),ord('Z')))
    # a while loop until user fill in everything
    while not submited:
        # clear screen change
        # powershell cls
        # linux clear
        os.system('cls')
        # printing heading
        print('input a genre and min vote number\n1:genre \t {}'.format(user_input[0]))
        print('2:min vote: \t {} \n3:submit \n4:back to main menu'.format(user_input[1]))
        # get user select which blank to type
        user_sel=input('> ')
        # check selection type/submit or back
        if user_sel == '1': #genre
            user_input[0]=input('> ')
            flaginput=False
            # validate input
            for i in range(len(user_input[0])):
                if ord(user_input[0][i]) not in valid_input1:
                    flaginput=True
                # fail clean input
                if flaginput: 
                    input('expecting a-z or A-Z,but something else found')
                    user_input[0]=''
        elif user_sel == '2':  # min vore
            user_input[1]=input('> ')
            try:
                usi1=int(user_input[1])
                if usi1<0:
                    raise Exception
            except:  # fail clearn input
                input('expecting positive or zero number,but something else found')
                user_input[1]=''
        elif user_sel == '3': # submit check
            if user_input[0]!='' and user_input[1]!='':
                submited=True
            else:
                print('fill the blank')
        elif user_sel == '4': # go back
            return
        else:
            input('type in 1,2,3 or 4')

    # check database inside, clean index
    collection = db['title_ratings']
    index_name=list(collection.index_information().keys())
    index_name.remove("_id_")
    if len(index_name)!=0:
        for i in range(len(index_name)):
            collection.drop_index(index_name[i])
    # create a new index to accelerate lookup
    collection.create_index([('tconst',-1)],name='tconst_-1')
    collection = db['title_basics']
    qurry=[
    {
        '$match': {
            'genres': {
                '$regex': user_input[0], 
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
        '$match': {
            'numVotes': {
                '$gte': int(user_input[1])
            }
        }
    }, {
        '$sort': {
            'averagRating': -1
        }
    }
]
    print('your result will be coming shortly.....')
    a=time.time()
    result=list(collection.aggregate(qurry)) 
    print('The result fetched in ',time.time() - a,' seconds, faster than 99% of computer on this plannet')
    input()
    # if not result it will be told a returned
    if len(result) == 0:
        print('No results return')
    else:
        datadisplay(result)
    db.title_ratings.drop_index('tconst_-1')
    return


def datadisplay(result):
    # get the tittle of the result
    a=list(result[0].keys())
    a.remove('_id')


    current_pg=0
    per_page=20
    max_pg=int(len(result)/per_page)
    if len(result)-max_pg*per_page !=0:
        max_pg+=1
    user_selection=None

    while user_selection!= '3':
        os.system('cls')
        string=''
        for i in range(len(a)):
            if a[i] in ['primaryTitle']:
                string=string+'{:<48} '.format(str(a[i]))
            elif a[i] in ['genres']:
                string=string+'{:<30} '.format(str(a[i]))
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
                    if type(result[index][a[i]])==list:
                        for x in range(len(result[index][a[i]])):
                            substring+=str(result[index][a[i]][x])+' '
                    else:
                        substring+=str(result[index][a[i]])+' '
                else:
                    substring+=str(result[index][a[i]])+' '
                
                if a[i] in ['primaryTitle']:
                    if len(substring)<48:
                        string=string+'{:<48} '.format(str(substring))
                    else:
                        string=string+'{:<46}.. '.format(str(substring[:46]))
                elif a[i] in ['genres']:
                    if len(substring)<36:
                        string=string+'{:<30} '.format(str(substring))
                    else:
                        string=string+'{:<28}.. '.format(str(substring[:28]))
                else:
                    if len(substring)<12:
                        string=string+'{:<12} '.format(str(substring))
                    else:
                        string=string+'{:<10}.. '.format(str(substring[:10]))

            print(string)
        print('result of {} to {} in page ({}/{})'.format(start, end, current_pg,max_pg))
        print('\n1:nextpage\n2:last page\n3:go back')
        user_selection=input('> ')
        if user_selection not in ['1','2','3']:
            input('unidentified')
        elif user_selection=='1' and current_pg<max_pg:
            current_pg+=1
        elif user_selection=='2' and current_pg>=1:
            current_pg-=1


if __name__ == '__main__':
    location='mongodb://localhost:27017'
    client = MongoClient(location)
    db=client["291db"]
    p2q2(db)

    client.close()
    