import  sys
import os 

# 获取当前目录
__dir__ = os.path.dirname(__file__)
up__dir__ = os.path.abspath(os.path.join(__dir__, '../'))
sys.path.append(up__dir__)
csv_dir =os.path.abspath(os.path.join(__dir__, './csv'))

from set_token import ts
pro = ts.pro_api()
columns = 'ts_code,exchange,chairman,manager,secretary,reg_capital,\
    setup_date,province,city,introduction,employees,main_business,\
    business_scope'
df = pro.stock_company(
    fields=columns
    )
df.to_csv("./csv/上市公司基本信息.csv")
