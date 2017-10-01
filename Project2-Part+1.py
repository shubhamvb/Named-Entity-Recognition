
# coding: utf-8

# In[65]:

def buildLangModel(filename):
    
    hmap = dict()
    counter = 0
    
    try:
        with open(filename, "r+") as f:
            for line in f:
                line1 = line.split()
                line2 = f.readline().split()
                #print(line1)
                #print(line2)
                line3 = f.readline().split()
                #print(line3)
                for i in range(len(line1)):   
                    if line1[i] in hmap:
                        hmap[line1[i]][line2[i]] = line3[i]
                    else:
                        hmap[line1[i]] = dict()
                        hmap[line1[i]][line2[i]] = line3[i]  
                                    
    except StopIteration:
        print("(End)")
    return hmap


def generateNER(hmap, filename):
    file = open("Project2Test.txt", "w")
    file.write("Type,Prediction")
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
                    
                    if line1[i] in hmap and line2[i] in hmap[line1[i]]:
                        string = hmap[line1[i]][line2[i]]
                        #print(line1[i],"-",line2[i],":", string)
                        if string == "B-MISC" or string == "I-MISC":
                            if string == "B-MISC":
                                misc_list.append(line3[i])
                            if string == "I-MISC" and prev == "B-MISC":
                                last = misc_list.pop()
                                last = last+"-"+line3[i]
                                misc_list.append(last)
                        elif string == "B-PER" or string == "I-PER":
                            if string == "B-PER":
                                per_list.append(line3[i])
                            if string == "I-PER" and prev == "B-PER":
                                last = per_list.pop()
                                last = last+"-"+line3[i]
                                per_list.append(last)
                        elif string == "B-ORG" or string == "I-ORG":
                            if string == "B-ORG":
                                org_list.append(line3[i])
                            if string == "I-ORG" and prev == "B-ORG":
                                last = org_list.pop()
                                last = last+"-"+line3[i]
                                org_list.append(last)
                        elif string == "B-LOC" or string == "I-LOC":
                            if string == "B-LOC":
                                loc_list.append(line3[i])
                            if string == "I-LOC" and prev == "B-LOC":
                                last = loc_list.pop()
                                last = last+"-"+line3[i]
                                loc_list.append(last)
                        elif string == "O":
                            misc_list.append(line3[i])
                        
                    else:
                        misc_list.append(line3[i])
                    prev = string
                   
    except StopIteration:
        print("(End)")
    
    print(len(misc_list))
    print(len(per_list))               
    print(len(org_list))               
    print(len(loc_list))

hmap = buildLangModel("/Users/shubhambarhate/Downloads/train.txt")
print("done")
print("--------------")
test_file = "/Users/shubhambarhate/Downloads/test.txt"
generateNER(hmap, test_file)


# In[ ]:



