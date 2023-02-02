import json

fr = open("./mydata/fund_data.json","r",encoding="utf8") 
fw = open("./mydata/fund_data2.json","w",encoding="utf8") 
data = json.load(fr)
for row in data:
    # print(row)
    fw.write(str(row)+"\n")


fr.close()
fw.close