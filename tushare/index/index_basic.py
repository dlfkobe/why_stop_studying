import  sys
import os 

# 获取当前目录
__dir__ = os.path.dirname(__file__)
print(__dir__)
up__dir__ = os.path.abspath(os.path.join(__dir__, '../'))
print(up__dir__)
sys.path.append(up__dir__)
csv_dir =os.path.abspath(os.path.join(__dir__, './csv'))

from set_token import ts
pro = ts.pro_api()
data = pro.index_basic(market="SSE")
#
data.to_csv("{}/上交所指数基本信息.csv".format(csv_dir))   
print("数据下载完成！")