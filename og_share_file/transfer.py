f_name=['name.basics.tsv','title.principals.tsv','title.basics.tsv','title.ratings.tsv']

for fn in f_name: 
    f = open(fn, "r")
    txt=f.readlines()
    f.close()

    head=txt[0].split('\t')
    head[-1]=head[-1][:-1]
    print(head)
    info=[]
    json_txt=[]
    for i in range(len(txt)):
        #formating
        info.append(txt[i].split('\t'))
        info[-1][-1]=info[-1][-1][:-1]
        #check for sub aray
        for x in range(len(info[-1])):
            info[-1][x]= info[-1][x].replace('[','{')
            info[-1][x]= info[-1][x].replace(']','}')
            info[-1][x]= info[-1][x].replace('\\N','NULL')
        
        

    for i in range(len(info)):
        print(len(txt))
        print(len(info))
        print(info[i])
        al_txt='{'
        for x in range(len(info[-1])):
            txt=''' "{}" : "{}",\n '''.format(head[x],info[i][x])
            al_txt+=txt

        al_txt=al_txt[:-2]+'}'
        print(al_txt)
        
        print('\n\n\n\n')
    


        
       



    print('\n\n\n\n')