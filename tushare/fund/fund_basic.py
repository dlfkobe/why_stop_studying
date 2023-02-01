import  sys
import os 
import pandas as pd

# 获取当前目录
__dir__ = os.path.dirname(__file__)
up__dir__ = os.path.abspath(os.path.join(__dir__, '../'))
sys.path.append(up__dir__)
csv_dir =os.path.abspath(os.path.join(__dir__, './csv'))

from set_token import ts
pro = ts.pro_api()
data = pro.fund_basic(market='E')
# data.index = pd.to_numeric(data.ts_code)
# data = data.sort_index()
data = data.sort_values(by='ts_code')

data.to_csv("{}/公募基金列表.csv".format(csv_dir))   
print("数据下载完成！")