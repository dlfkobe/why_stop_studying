import  sys
import os 

# 获取当前目录
__dir__ = os.path.dirname(__file__)
up__dir__ = os.path.abspath(os.path.join(__dir__, '../'))
sys.path.append(up__dir__)
csv_dir =os.path.abspath(os.path.join(__dir__, './csv'))

from set_token import ts
pro = ts.pro_api()

# 公告日期范围,只看今年范围内公告的管理层
start_date = "20220101"
end_date = "20230101"
columns = ''
df = pro.stk_managers(start_date=start_date,end_date=end_date)
df.to_csv("{}/上市公司管理层.csv".format(csv_dir))