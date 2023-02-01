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
 
def get_fund(fund_code):    
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
        print(list(one_person))
        return [True,one_person]
        


# 加载基金详情中csv，读取到基金代码
path = "{}/公募基金列表1.csv".format(csv_dir)
# 使用pandas读入
data = pd.read_csv(path) #读取文件中所有数据
result =[]
# 遍历每一行
for index,row in data.iterrows():
    code = row['ts_code']
    print(code)
    flag,manager = get_fund(code)
    if  not flag :
        continue
    print(manager)
    a = list(row)
    print(a)
    a.extend(manager)
    result.append(a)
    # row.append(manager)
    # r = pd.merge(row, manager,left_index=True,right_index=True)
    # print("合并结果为：",r)
    # pd.concat(result,r)
print("结果为：\n",result)
    
    
a = get_fund("1500011.SZ")
    
