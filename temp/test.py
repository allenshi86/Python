#!/usr/bin/env python3
import json

from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.charts import Line

# V1 版本开始支持链式调用
'''
bar = (
    Bar()
    .add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
    .add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
    .add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
    .set_global_opts(title_opts=opts.TitleOpts(title="某商场销售情况"))
)
bar.render()


# 不习惯链式调用的开发者依旧可以单独调用方法
bar = Bar()
bar.add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
bar.add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
bar.add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
bar.set_global_opts(title_opts=opts.TitleOpts(title="某商场销售情况"))
bar.render()
'''
'''
line = Line()
line.add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
line.add_yaxis("", [114, 55, 27, 101, 125, 27, 105])
line.set_global_opts(title_opts=opts.TitleOpts(title="AP负载"))
line.render()
'''
'''
fruits = ['苹果', '香蕉', '凤梨', '桔子', '橙', '桃子']
shop1_sales = [8888, 3323, 6989, 8873, 3876, 15409]
shop2_sales = [4888, 7023, 3989, 5873, 8876, 6409]

line = (
    Line()
    .add_xaxis(fruits)
    .add_yaxis("商家A", shop1_sales)
    .add_yaxis("商家B", shop2_sales, is_smooth=True)
    .set_global_opts(title_opts=opts.TitleOpts(title="水果加个"))

)

line.render(path='/Users/momo/github/django-wireless/proj_wireless/templates/rend.html')
'''


a = [{'id': 2679, 'ap_name': 'T1-F16-AP08', 'query_time': '2021-10-12 18:44:23'}, {'id': 2752, 'ap_name': 'T1-F16-AP09', 'query_time': '2021-10-12 18:44:57'}, {'id': 2825, 'ap_name': 'T1-F16-AP10', 'query_time': '2021-10-12 18:52:39'}]

#a =[1,2,3,4]
b = a.reverse()

print(a)