# -*- coding : utf-8 -*-
# Converting JSON file to csv file
import  json
import  sys
import  re

argvs = sys.argv


file = argvs[1]
out = re.sub(r'json','txt',file)

f = open (file,'r')

jsonData = json.load(f)
f.close()

o = open(out,'w')

w = jsonData['storage']['storage']['weight']
list_id = jsonData['storage']['storage']['weight'].keys()
list_label = jsonData['storage']['label']['label_count'].keys()
head = "id"

for label in list_label:
    head += "\t"
    head += label

head += "\n"
o.write(head)

for id in list_id:
    string = ""
    for label in list_label:
        weight = w[id].get(label)["v1"] if w[id].get(label) != None else "ND"
        string += "\t"
        string += str(weight)

    id = re.sub(r'[@num]', '', id)
    tex = id + string + "\n"
    o.write(tex)