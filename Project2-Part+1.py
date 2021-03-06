
# coding: utf-8

# In[119]:

def buildLangModel(filename):
    
    hmap = dict()
    counter = 0
    
    try:
        with open(filename, "r+") as f:
            for line in f:
                line1 = line.split()
                line2 = f.readline().split()
                line3 = f.readline().split()
                
                for i in range(len(line1)):   
                    if line1[i] in hmap:
                        hmap[line1[i]][line2[i]] = line3[i]
                    else:
                        hmap[line1[i]] = dict()
                        hmap[line1[i]][line2[i]] = line3[i]  
                                    
    except StopIteration:
        print("Dataset not in appropriate chunk size")
    return hmap


def check(string, prev, string1, string2, ner_list, word_number):
    if string == string1:
        ner_list.append(word_number+"-"+word_number)
    if string == string2 and prev == string1:
        last = ner_list.pop()
        last = last+"-"+word_number
        ner_list.append(last)
    
    return ner_list

def generateNER(hmap, filename):
    org_list = []
    per_list = []
    loc_list = []
    misc_list = []
    
    try:
        with open(filename, "r+") as f:
            for line in f:
                prev = ""
                string = ""
                line1 = line.split()
                line2 = f.readline().split()
                line3 = f.readline().split()
                for i in range(len(line1)):   
                    #print(line1[i])
                    if line1[i] in hmap and line2[i] in hmap[line1[i]]:
                        string = hmap[line1[i]][line2[i]]
                        #print(string)    
                        if string == "B-PER" or string == "I-PER":
                            per_list = check(string, prev, "B-PER", "I-PER", per_list, line3[i])
                        
                        elif string == "B-ORG" or string == "I-ORG":
                            org_list = check(string, prev, "B-ORG", "I-ORG", org_list, line3[i])
                            
                        elif string == "B-LOC" or string == "I-LOC":
                            loc_list = check(string, prev, "B-LOC", "I-LOC", loc_list, line3[i])    
                        
                        elif string == "B-MISC" or string == "I-MISC":
                            misc_list = check(string, prev, "B-MISC", "I-MISC", misc_list, line3[i])
                                
                        
                    elif line1[i][0].isupper() and line2[i].startswith("NN"):
                        
                        misc_list.append(line3[i]+"-"+line3[i])
                        

                        
                    prev = string
                   
    except StopIteration:
        print("(End)")
    
    return misc_list, per_list, org_list, loc_list

def generateTextFile(misc_list, per_list, org_list, loc_list, filename):
    file = open(filename, "w")
    file.write("Type,Prediction\n")
    
    file.write("ORG,")
    for i in range(len(org_list)):
        file.write(org_list[i]+" ")
    file.write("\n")
    
    file.write("MISC,")
    for i in range(len(misc_list)):
        file.write(misc_list[i]+" ")
    file.write("\n")
    
    file.write("PER,")
    for i in range(len(per_list)):
        file.write(per_list[i]+" ")
    file.write("\n")
    
    file.write("LOC,")
    for i in range(len(loc_list)):
        file.write(loc_list[i]+" ")
    
    file.close()
    
hmap = buildLangModel("/Users/shubhambarhate/Downloads/train.txt")
print("Hmap generation Complete")
print("--------------")
test_file = "/Users/shubhambarhate/Downloads/test.txt"
misc_list, per_list, org_list, loc_list = generateNER(hmap, test_file)
output_test_file = "Oct1Test3.txt"
generateTextFile(misc_list, per_list, org_list, loc_list, output_test_file)
print(len(misc_list)+len(per_list)+len(org_list)+len(loc_list))
print("File Write complete")


# In[ ]:



