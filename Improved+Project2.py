
# coding: utf-8

# In[9]:

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
                        if line3[i] in hmap[line1[i]]:
                            hmap[line1[i]][line3[i]] += 1 
                        else:
                            hmap[line1[i]][line3[i]] = 1 
                    else:
                        hmap[line1[i]] = dict()
                        hmap[line1[i]][line3[i]] = 1
                                    
    except StopIteration:
        print("Dataset not in appropriate chunk size")
    
    for i in hmap:
        max_count = 0
        desired_value = ""
        for j in hmap[i]:
            if hmap[i][j] > max_count:
                max_count = hmap[i][j]
                desired_value = j 
        hmap[i] = desired_value

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
                    
                    if line1[i] in hmap:
                        if "PER" in hmap[line1[i]]:
                            per_list.append(line3[i] + "-" + line3[i] + " ")
                        if "LOC" in hmap[line1[i]]:
                            loc_list.append(line3[i] + "-" + line3[i] + " ")
                        if "ORG" in hmap[line1[i]]:
                            org_list.append(line3[i] + "-" + line3[i] + " ")
                        if "MISC" in hmap[line1[i]]:
                            misc_list.append(line3[i] + "-" + line3[i] + " ")
                    
                    else:
                        if line1[i].isupper() and len(line1[i])>3:
                            loc_list.append(line3[i] + "-" + line3[i] + " ")
                        elif line1[i][0].isupper():
                            per_list.append(line3[i] + "-" + line3[i] + " ")
                    
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
output_test_file = "Oct1Test6.txt"
generateTextFile(misc_list, per_list, org_list, loc_list, output_test_file)
print(len(misc_list)+len(per_list)+len(org_list)+len(loc_list))
print("File Write complete")


# In[ ]:



