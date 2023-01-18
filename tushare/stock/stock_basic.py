import  sys
import os 

# 获取当前目录
__dir__ = os.path.dirname(__file__)
up__dir__ = os.path.abspath(os.path.join(__dir__, '../'))
sys.path.append(up__dir__)
csv_dir =os.path.abspath(os.path.join(__dir__, './csv'))

from set_token import ts
pro = ts.pro_api()

# 数据调取
data = pro.query("stock_basic",list_status='L',fields='ts_code,symbol,name,area,industry,fullname,market,exchange,list_date,is_hs')
data.to_csv('./csv/股票列表.csv')
# print(data)

