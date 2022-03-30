import json,sys

# a function that transfering each file to json file
def tsv2json(input_file,output_file):
    arr = []
    try:
        file = open(input_file, 'r')
        a = file.readline()
    except:
        print("failed to open {}.".format(input_file))
    
    # The first line consist of headings of the record 
    # so we will store it in an array and move to 
    # next line in input_file.
    titles = [t.strip() for t in a.split('\t')]
    for line in file:
        d = {}
        for t, f in zip(titles, line.split('\t')):
            # replace some of the elements in the list
            f=f.strip().replace('\\N','NULL')
            f=f.strip().replace('[','')
            f=f.strip().replace(']','')
            f=f.strip().replace('"','')
            if ',' in f and t in ['primaryProfession','knownForTitles','genres','characters']:
                d[t] = [c.strip() for c in f.split(',')]
            else:
                # Convert each row into dictionary with keys as titles
                d[t] = f.strip()
            
        # we will use strip to remove '\n'.
        arr.append(d)
        # we will append all the individual dictionaires into list 
        # and dump into file.
    try:
        with open(output_file, 'w', encoding='utf-8') as output_file:
            output_file.write(json.dumps(arr, indent=4))
    except Exception as e:
        print(e)
    print("output_file",output_file)

# user input
# if typed python3 tsv-2-json.py
# it will us: python3 transfer_off.py name.basics.tsv title.basics.tsv title.principals.tsv title.ratings.tsv
# otherwise it will load user requestd file
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(" transcoding:\n name.basics.tsv \n title.basics.tsv\n title.principals.tsv\n title.ratings.tsv ")
        list_of_file=['name.basics.tsv','title.basics.tsv','title.principals.tsv','title.ratings.tsv']
    else:
        # python3 transfer_off.py name.basics.tsv title.basics.tsv title.principals.tsv title.ratings.tsv
        list_of_file=[]
        print(" transcoding:")
        for i in range(1,len(sys.argv)):
            list_of_file.append(sys.argv[i])
            print(" {} ".format(sys.argv[i]))
    print('-'*12)
    for i in range(len(list_of_file)):
        input_filename = list_of_file[i]
        output_filename = input_filename[:-4]+'.json'
        tsv2json(input_filename,output_filename)