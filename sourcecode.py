from pymongo import MongoClient
import sys,os


def search_title(db):
    os.system('cls')
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


def character(tt, db):
    principals = db['title_principals']
    caster = db['name_basics']
    # find the corresponding principals of the seleted movie
    find_character = principals.find({'tconst': tt}, {'_id': 0, 'nconst': 1, 'characters': 1})
    for each in find_character:
        nm = each.get('nconst')
        check = each.get('characters')
        # find the name for caster
        find_caster = caster.find({'nconst': nm}, {'_id': 0, 'primaryName': 1})
        if check != 'NULL':
            for name in find_caster:
                # one cast might play multi roles, print it separately to avoid error
                if type(check) != list:
                    print(name.get('primaryName') + ' plays the role of ' + check)
                else:
                    print(name.get('primaryName') + ' plays the role of ' + ', '.join(check))


def search_genres(db):
    os.system('cls')
    input('2')


def search_caster(db):
    os.system('cls')
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
        if type(l) != list:
            print(str(index) + '. ' + each.get('primaryName') + ': ' + l)
        else:
            print(str(index) + '. ' + each.get('primaryName') + ': ' + ', '.join(l))
        choice.append(str(index))
        finded.append(each)
        index = index + 1

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


def add_movie(db):
    os.system('cls')
    input('4')


def add_castre(db):
    os.system('cls')
    input('5')


def menu(db):
    while db is not None:
        print('''
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