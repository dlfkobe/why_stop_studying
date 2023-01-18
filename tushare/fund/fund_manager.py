import  sys
import os 

# 获取当前目录
__dir__ = os.path.dirname(__file__)
up__dir__ = os.path.abspath(os.path.join(__dir__, '../'))
sys.path.append(up__dir__)
csv_dir =os.path.abspath(os.path.join(__dir__, './csv'))

from set_token import ts
pro = ts.pro_api()
data = pro.fund_manager()
data.to_csv("{}/基金经理.csv".format(csv_dir))   
print("数据下载完成！")