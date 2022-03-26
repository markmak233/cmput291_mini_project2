from pymongo import MongoClient
import sys,os


def search_title(db):
    os.system('cls')
    title = db['title_basics']
    rating = db['title_ratings']

    search = input("Please enter what title you want to search (all variable should be separated by space): ").split()

    key = '\"\"'
    key = "\"" + key.join(search) + "\""

    title.drop_indexes()
    title.create_index([("primaryTitle", "text"), ("startYear", "text")])
    find = title.find({"$text": {"$search": key}})
    find_list = []
    for each_find in find:
        find_list.append(each_find)

    choice = []
    index = 1
    for each_result in find_list:
        print(str(index) + ". " + str(each_result))
        choice.append(str(index))
        index = index + 1
    # select the movie
    select = input("Which movie you want to search (Enters the leading number): ")
    while select not in choice:
        print("The number input exceed the limit! Please try again.")
        select = input("Which movie you want to search (Enters the leading number): ")

    selected = find_list[int(select)-1]
    selected_tt = selected.get('tconst')

    # get the rating
    find_rating = rating.find({'tconst': selected_tt}, {'_id': 0, 'averageRating': 1, 'numVotes': 1})
    for f in find_rating:
        print('\nMovie title: ' + selected.get('primaryTitle') + '\nRating: ' + f.get('averageRating') +
              '\nNumber of votes: ' + f.get('numVotes'))

    character(selected_tt, db)

    input("\n\nPress enter to return to main menu.")


def character(tt, db):
    principals = db['title_principals']
    caster = db['name_basics']

    find_character = principals.find({'tconst': tt}, {'_id': 0, 'nconst': 1, 'characters': 1})
    for each in find_character:
        nm = each.get('nconst')
        check = each.get('characters')
        find_caster = caster.find({'nconst': nm}, {'_id': 0, 'primaryName': 1})
        if check != 'NULL':
            for name in find_caster:
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
    principle = db['title_principles']

    search = input("Please enter which caster you want to search: ")

    find = caster.find({'primaryName': {'$regex': search, '$options': 'i'}})
    finded = []
    choice = []
    index = 1
    for each in find:
        print(str(index) + '. ' + each.get('primaryName') + ': ' + ', '.join(each.get('primaryProfession')))
        choice.append(str(index))
        finded.append(each)
        index = index + 1

    print(choice)
    print(finded)

    which = input("Which caster you want to view (Enter the leading number): ")
    while which not in choice:
        print("The choice does not exist, please try again")
        which = input("Which caster you want to view (Enter the leading number): ")

    selected = finded[int(which)-1]
    print(selected)

    selected_nm = selected.get('nconst')
    selected_tt = selected.get('knownForTitles')

    find_movie = principle.find({'nconst': selected_nm})
    print(find_movie)


    input()


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