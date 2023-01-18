import tushare as ts 

ts.set_token("6cd6dd59e845ac7cddb9cefea7f56518cf821b545a42c9092dba354a")
pro = ts.pro_api()

# 数据调取
data = pro.query("stock_basic",list_status='L',fields='ts_code,symbol,name,area,industry,fullname,market,exchange,list_date,is_hs')
data.to_csv('./csv/股票列表.csv')
# print(data)

