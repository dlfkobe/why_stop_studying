# import json

# import pandas as pd

# # 读取CSV文件
# csvData = pd.read_csv(r'./mydata/cb.csv', header = 0)  

# # 读取CSV文件包含的列名并转换为list
# columns = csvData.columns.tolist()

# # 创建空字典
# outPut = {}

# # 将CSV文件转为字典
# for col in columns:
# 	outPut[col] = str(csvData.loc[0, col]) # 这里一定要将数据类型转成字符串，否则会报错

# # 将字典转为json格式
# jsonData = json.dumps(outPut) # 注意此处是dumps，不是dump

# # 保存json文件
# with open(r'./mydata/testData.json', 'w',encoding='utf-8') as jsonFile:
# 	jsonFile.write(jsonData)

import json
fo=open("./mydata/fund.csv","r",encoding="utf8")  #打开csv文件
ls=[]
for line in fo:
    line=line.replace("\n","")  #将换行换成空
    ls.append(line.split(","))  #以，为分隔符
fo.close()  #关闭文件流
fw=open("./mydata/fund_data.json","w",encoding="utf8")  #打开json文件
for i in range(1,len(ls)):  #遍历文件的每一行内容，除了列名
    ls[i]=dict(zip(ls[0],ls[i]))  #ls[0]为列名，所以为key,ls[i]为value,
    #zip()是一个内置函数，将两个长度相同的列表组合成一个关系对
json.dump(ls[1:],fw,sort_keys=True,indent=4,ensure_ascii=False)
#将Python数据类型转换成json格式，编码过程
# 默认是顺序存放，sort_keys是对字典元素按照key进行排序
#indet参数用语增加数据缩进，使文件更具有可读性
fw.close()
