# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
# 设置一些全局的资源参数，可以进行个性化修改
import matplotlib
# 设置图片尺寸 14" x 7"
# rc: resource configuration
matplotlib.rc('figure', figsize = (14, 7))
# 设置字体 14
matplotlib.rc('font', size = 14)
# 不显示顶部和右侧的坐标线
matplotlib.rc('axes.spines', top = False, right = False)
# 不显示网格
matplotlib.rc('axes', grid = False)
# 设置背景颜色是白色
matplotlib.rc('axes', facecolor = 'white')

import pandas as pd 
import time
import datetime

start = time.clock()
LC = pd.read_csv("C:\\Users\\skyamz\\Desktop\\ppdai_3_213\\LC.csv",sep=',')  # names=  encoding=   ,usecols=range(10)
LP = pd.read_csv("C:\\Users\\skyamz\\Desktop\\ppdai_3_213\\LP.csv",sep=',')
def cla(n,lim):  # map function  n是年龄值，lim是每个年龄段的长度
    return'[%.f,%.f)'%(lim*(n//lim),lim*(n//lim)+lim) 
LC['age_range'] = pd.Series([cla(s,5) for s in LC['年龄']])
data = pd.merge(LC,LP,how='outer',on='ListingId')
data['借款成功日期'] = pd.to_datetime(data['借款成功日期'])
data['到期日期'] = pd.to_datetime(data['到期日期'])
data['还款日期'] = data['还款日期'].replace('\\N','2017-02-22')
data['还款日期'] = pd.to_datetime(data['还款日期'])
#0-‘未还款’，1-‘已正常还款’，2-‘已逾期还款’，3-‘已提前还清该标全部欠款’，4-‘已部分还款’
#按年龄范围来画图
total =data.groupby(LC['age_range'])['借款金额'].sum()
payall = data[data['还款状态']==3].groupby(LC['age_range'])['应还本金'].sum()
Rpayall = payall/total
paypart = data[data['还款状态']==4].groupby(LC['age_range'])['应还本金'].sum()-data[data['还款状态']==4].groupby(LC['age_range'])['剩余本金'].sum()
Rpaypart = paypart/total
paynone = data[data['还款状态']==2].groupby(LC['age_range'])['应还本金'].sum() +data[(data['还款状态']==4)&(data['还款日期']>data['到期日期'])].groupby(LC['age_range'])['剩余本金'].sum()
Rpaynone = paynone/total
bar_heights =  pd.concat([Rpayall, Rpaypart, Rpaynone], axis=1)

N = 9
ind = np.arange(N)+0.35
width = 0.15     
payall = (0.019337, 0.016318, 0.014620, 0.015832, 0.015897, 0.016230, 0.013456, 0.023020, 0.004602)
fig, ax = plt.subplots()
rects1 = ax.bar(ind, payall, width, color='b')

paypart = (0.000169, 0.000099, 0.000080, 0.000070, 0.000059, 0.000021, 0.000228, 0.000242, 0.000054)
rects2 = ax.bar(ind+width, paypart, width, color='y')

paynone = (0.014230, 0.014139, 0.015019, 0.013996, 0.014256, 0.013324, 0.016214, 0.011145, 0.010216)
rects3 = ax.bar(ind+width*2, paynone, width, color='r')

# add some
ax.set_ylabel('account')
ax.set_title('the proportion of different age groups')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('[15,20)','[20,25)','[25,30)','[30,35)','[35,40)','[40,45)','[45,50)','[50,55)','[55,60) '),rotation=45 )

ax.legend( (rects1[0], rects2[0], rects3[0]), ('payall', 'paypart','paynone') )

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., height, '%.4f'%float(height),
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)
plt.show()