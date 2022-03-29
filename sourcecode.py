from pymongo import MongoClient
import sys,os


def search_title(db):
    os.system('clear')
    title = db['title_basics']
    rating = db['title_ratings']

    # asking for title name
    search = input("Please enter what title you want to search (all variable should be separated by space): ").split()
    # combine the input into a key for search
    key = '\"\"'
    key = "\"" + key.join(search) + "\""
    # using index to search the input case-insensitive
    title.drop_indexes()
    title.create_index([("primaryTitle", "text"), ("startYear", "text")])
    find = title.find({"$text": {"$search": key}})
    # put all the result find into a list
    find_list = []
    for each_find in find:
        find_list.append(each_find)

    if len(find_list) == 0:
        input("Invalid input!  \nPlease try to re-enter.")
        os.system('clear')
        return

    # putting ordering at the front of each movie
    choice = []
    index = 1
    for each_result in find_list:
        print(str(index) + ". " + str(each_result))
        choice.append(str(index))
        index = index + 1
    # select the movie
    select = input("\nWhich movie you want to search (Enters the leading number): ")
    while select not in choice:
        print("The number input exceed the limit! Please try again.")
        select = input("\nWhich movie you want to search (Enters the leading number): ")
    # the ordering of the numbers should match the ordering of the find list
    # then we get the index of choice list to find the result in find list
    selected = find_list[int(select)-1]
    selected_tt = selected.get('tconst')

    # get the rating and number of votes
    find_rating = rating.find({'tconst': selected_tt}, {'_id': 0, 'averageRating': 1, 'numVotes': 1})
    for f in find_rating:
        print('\nMovie title: ' + selected.get('primaryTitle') + '\nRating: ' + f.get('averageRating') +
              '\nNumber of votes: ' + f.get('numVotes'))

    character(selected_tt, db)

    input("\n\nPress enter to return to main menu.")
    os.system('clear')
    return


def character(tt, db):
    principals = db['title_principals']
    caster = db['name_basics']
    # find the corresponding principals of the seleted movie
    find_character = principals.find({'tconst': tt}, {'_id': 0, 'nconst': 1, 'job': 1, 'characters': 1})
    for each in find_character:
        nm = each.get('nconst')
        check_char = each.get('characters')
        job_check = each.get('job')
        # find the name for caster
        find_caster = caster.find({'nconst': nm}, {'_id': 0, 'primaryName': 1})
        if check_char != 'NULL':
            for name in find_caster:
                # one cast might play multi roles, print it separately to avoid error
                if type(check_char) != list:
                    print(name.get('primaryName') + ' plays the role of ' + check_char)
                else:
                    print(name.get('primaryName') + ' plays the role of ' + ', '.join(check_char))
        elif job_check != 'NULL':
            for name in find_caster:
                print(name.get('primaryName') + ' have a job of ' + job_check)


def search_genres(db):
    # set up user input 
    user_sel=None
    user_input=['','0']
    submited=False
    valid_input1=list(range(ord('a'),ord('z')))+list(range(ord('A'),ord('Z')))
    # a while loop until user fill in everything
    while not submited:
        # clear screen change
        # powershell clear
        # linux clear
        os.system('clear')
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
    print('your result will be coming shortly.....(est. 5 seconds)')
    result=list(collection.aggregate(qurry)) 
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
        os.system('clear')
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


def search_caster(db):
    os.system('clear')
    caster = db['name_basics']
    principle = db['title_principals']
    basics = db['title_basics']
    # search for the caster
    search = input("Please enter which caster you want to search: ")
    find = caster.find({'primaryName': {'$regex': search, '$options': 'i'}})
    finded = []
    choice = []
    index = 1
    # print the caster with their profession and let user choice
    for each in find:
        l = each.get('primaryProfession')
        print(l,type(l),len(l))
        if len(l) == 0:
            print(str(index) + '. ' + each.get('primaryName') + ':no profession')
        elif type(l) != list:
            print('0')
            print(str(index) + '. ' + each.get('primaryName') + ': ' + l)
        else :
            print('2')
            print(str(index) + '. ' + each.get('primaryName') + ': ' + ', '.join(l))
        choice.append(str(index))
        finded.append(each)
        index = index + 1

    if len(finded) == 0:
        input("Invalid input! \nPlease try to re-enter.")
        os.system('clear')
        return

    which = input("\nWhich caster you want to view (Enter the leading number): ")
    while which not in choice:
        print("The choice does not exist, please try again")
        which = input("\nWhich caster you want to view (Enter the leading number): ")

    # using the corresponding nconst to find the movie caster worked for
    selected = finded[int(which)-1]
    selected_nm = selected.get('nconst')
    find_movie = principle.find({'nconst': selected_nm}, {'_id': 0, 'job': 1, 'characters': 1, 'tconst': 1})

    print("\nThis caster have jobs in the movie: ")
    for f in find_movie:
        title = f.get('tconst')
        find_title = basics.find({'tconst': title}, {'_id': 0, 'primaryTitle': 1})
        for i in find_title:
            characters = f.get('characters')
            job = f.get('job')
            # if the characters' field for that movie is null then exclude it
            if characters == 'NULL':
                print("Movie Title: " + i.get('primaryTitle') +
                      "\nJob: " + job
                      )
            # if the jobs' field for that movie is null then exclude it
            elif job == 'NULL':
                if type(characters) != list:
                    print("Movie Title: " + i.get('primaryTitle') +
                          "\nCharacters: " + f.get('characters'))
                else:
                    print("Movie Title: " + i.get('primaryTitle') +
                            "\nCharacters: " + ', '.join(f.get('characters')))
            # if the characters' field and jobs' field for that movie is null then include it to tell the user
            # if the characters' field and jobs' field for that movie is not null then print it normally
            else:
                if type(characters) != list:
                    print("Movie Title: " + i.get('primaryTitle') +
                          "\nJob: " + job +
                          "\nCharacters: " + f.get('characters')
                          )
                else:
                    print("Movie Title: " + i.get('primaryTitle') +
                            "\nJob: " + job +
                            "\nCharacters: " + ', '.join(f.get('characters'))
                    )
        print('\n')

    input("\nPress enter to return to the main menu.")
    os.system('clear')
    return


def add_movie(db):
    os.system('clear')
    

    title_basics_collection = db.get_collection("title_basics")
    #add movie
    try:
        #ask user to input info for the movie
        print("Please input the infomation for the movie:")
        movie_id = input("movie_id:")
        title = input("movie_title:")
        start_year = input("start_year:")
        running_time = input("running_time:")
        temp = input("a_list_of_geners:(Please use ',' to separate every genres)")
        a_list_of_genres = temp.split(sep = ',')
        col = {"tconst":movie_id,
            "titleType":"movie",
            "primaryTitle":title,
            "originalTitle":title,
            "isAdult":"Null",
            "startYear":start_year,
            "endYear":"Null",
            "runtimeMinutes":running_time,
            "geners":a_list_of_genres
            }
        result = title_basics_collection.insert_one(col)
        print(result.inserted_id)
    except Exception as e:
        print("Error{}".format(e))


def add_castre(db):
    os.system('clear')
    
    title_principals_collection = db.get_collection("title_principals")
    title_basics_collection = db.get_collection("title_basics")
    name_basics_collection = db.get_collection("name_basics")

    #user input

    try:
        #enter a mem id and check whether it exists in name collection
        
        member_id = input("Please enter Info for a cast/crew member: \nMember_id:")
        queryCondition1 = {"nconst":member_id}
        related_name = name_basics_collection.find(queryCondition1)
        find_list = []
        for i in related_name:
            find_list.append(i)
        while(len(find_list) == 0):
            input("Invalid input! There doesn't exist same member_id in name_basics_collection \nPlease try to re-enter.")
            os.system('clear')

            
            member_id = input("Please enter Info for a cast/crew member: \nMember_id:")
            queryCondition1 = {"nconst":member_id}
            related_name = name_basics_collection.find(queryCondition1)
            find_list = []
            for i in related_name:
                find_list.append(i)
        #enter a title id and check whether it exists in title collection
        title_id = input("title_id:")
        queryCondition2 = {"tconst":title_id}
        related_title = title_basics_collection.find(queryCondition2)
        find_list = []
        for i in related_title:
            find_list.append(i)
        while(len(find_list) == 0):
            input("Invalid input! There doesn't exist same title_id in title_basics_collection \nPlease try to re-enter.")
            os.system('clear')
            print("Please enter Info for a cast/crew member: \nmember_id:",member_id)
            title_id = input("title_id:")
            queryCondition2 = {"tconst":title_id}
            related_title = title_basics_collection.find(queryCondition2)
            find_list = []
            for i in related_title:
                find_list.append(i)

        a_category = input("Category:")
        


        #find max order
        
        related_title = title_principals_collection.find(queryCondition2)
        find_list = []
        for i in related_title:
            find_list.append(int(i.get('ordering')))
        if(len(find_list) == 0):
            correct_max_order = 1
        else:
            correct_max_order = str(max(find_list) + 1)
        print("ordering:",correct_max_order)
        
        
        temp = input("/////////////////////////////////\nDo you want to insert more infomation for the crew member, such as 'job' and 'characters'?. \nPlease enter 'Y/y' for 'Yes' AND 'N/n' for 'No'.\n(If say no, they will be set to 'Null' by default).\nYour choice:")
        temp1 = True
        while(temp1):

            if(temp == 'Y' or temp =='y'):
                os.system('clear')
                print("Please enter Info for a cast/crew member: \nmember_id:",member_id,"\ntitle_id:",title_id,"\nordering:",correct_max_order,"\ncategory:",a_category)

                temp_job = input("member's job:")
                temp_char = input("member's characters:")

                col = {"tconst":title_id,
                    "ordering":correct_max_order,
                    "nconst":member_id,
                    "category":a_category,
                    "job" : "Null",
                    "characters" : "Null"
                    }
                temp1 = False
            elif(temp == 'N' or temp == 'n'):
                col = {"tconst":title_id,
                "ordering":correct_max_order,
                "nconst":member_id,
                "category":a_category,
                "job" : "Null",
                "characters" : "Null"
                }
                temp1 = False
            else:
                input("Please input valid character. Press enter to re-enter.")
                os.system('clear')
                print("Please enter Info for a cast/crew member: \nmember_id:",member_id,"\ntitle_id:",title_id,"\nordering:",correct_max_order,"\ncategory:",a_category)

                temp = input("Do you want to insert info of 'job' and 'characters' for the cast/crew member. \nplease enter 'Y/y' OR 'N/n'.\n If no, they will be set to 'Null'")

        result = title_principals_collection.insert_one(col)
        input("Info is inserted successfully! Please press 'Enter' back to the menu.")
        os.system('clear')

    




    except Exception as e:
        print("Error".format(e))


def menu(db):
    while db is not None:
        os.system('clear')
        print('''
        User Menu:
        
        1.Search for titles 
        2.Search for genres
        3.Search for cast/crew members
        4.Add a movie
        5.Add a cast/crew member
        6.exit\n
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


def main():
    db=None
    try:
        location='mongodb://localhost:'+str(int(sys.argv[1]))
        client = MongoClient(location)
        db = client["291db"]
    except Exception as e:
        print("fail to connect ",location)
    menu(db)


if __name__ == "__main__":
    if len(sys.argv)!=2:
        print("ex. Python3 sourcecode 27017")
    else:
        main()
