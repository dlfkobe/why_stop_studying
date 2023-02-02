import  sys
import os 
import csv
import pandas as pd
# 获取当前目录
__dir__ = os.path.dirname(__file__)
up__dir__ = os.path.abspath(os.path.join(__dir__, '../'))
sys.path.append(up__dir__)
csv_dir =os.path.abspath(os.path.join(__dir__, './csv'))

from set_token import ts
pro = ts.pro_api()

# 获取单个基金的信息
 
def get_fund_manager(fund_code):    
    # 获取基金经理信息，以及开始管理该基金的日期
    df_manager = pro.fund_manager(ts_code=fund_code)
    # print(df_manager)
    if df_manager.empty:
       return [False,0]
    else:
        df_manager = df_manager.sort_values('begin_date',ascending=False)
        # print(type(df_manager))
        # for i in df_manager:
        #   print(i)
        one_person = df_manager.iloc[0]
        # print(list(one_person))
        return [True,one_person]
    
# def get_fund_company(fund_code):    
#     # 获取基金经理信息，以及开始管理该基金的日期
#     df_company = pro.fund_manager(ts_code=fund_code)
#     # print(df_manager)
#     if df_manager.empty:
#        return [False,0]
#     else:
#         df_manager = df_manager.sort_values('begin_date',ascending=False)
#         # print(type(df_manager))
#         # for i in df_manager:
#         #   print(i)
#         one_person = df_manager.iloc[0]
#         print(list(one_person))
#         return [True,one_person]
        


# 加载基金详情中csv，读取到基金代码
path = "{}/公募基金列表1.csv".format(csv_dir)
# 结果
result =[]
# 遍历每一行
headers = []

with open(path, 'r',encoding='utf-8') as f:
    reader = csv.reader(f)
    headers_1 = next(reader)
    headers_2 = ["ts_code","ann_date","name","gender","birth_year","edu","nationality","begin_date","end_date","resume"]
    headers.extend(headers_1)
    headers.extend(headers_2)
    print(headers)
    
    for row in reader:
        # print(row)

        code = row[1]
        # print(code)
        flag,manager = get_fund_manager(code)
        if  not flag :
            continue
        # print(manager)
        row.extend(manager)
        result.append(row)
    

# print("结果为：\n",result)
test = pd.DataFrame(columns=headers,data=result)
test.to_csv('testcsv.csv',encoding='utf-8')
print("转换完成！")
    
    
