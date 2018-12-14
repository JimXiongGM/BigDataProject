import tushare as ts
import os

ts.set_token('32841c8a92c5151ef0d552c3a23ebeeb5514325e95d1ea15025868da')#设置token，只需设置一次
pro = ts.pro_api()

pro.get_hist_d

def fun1():
    stock_pool = ['603912.SH','300666.SZ','300618.SZ','002049.SZ','300672.SZ']

    df = pro.daily(ts_code='603912.SH',  start_date='20180901', end_date='20181001')

    #df = pro.trade_cal(exchange='', start_date='20180901', end_date='20181001', \
    # fields='exchange,cal_date,is_open,pretrade_date', is_open='0')

    print (df.ix[2])
    print (df.ix[3])

if __name__ == "__main__":
    fun1()