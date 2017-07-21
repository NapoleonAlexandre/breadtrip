# coding=utf-8

## Author: Jiahao Wang (Frank)
#  Date: 2017.11
#  Email: sb418723601@gmail.com
#  本脚本为批处理旅行日志csv文件并调用百度地图API实现数据可视化
#  注:此脚本包含私人使用的百度地图API Key，请勿滥用，禁止在没有作者授权下私自分享。大规模使用时请使用自己的API Key。


import urllib.request;
import csv;
import glob;


# def txt_wrap_by(start_str, end, html):
#     start = html.find(start_str)
#     if start >= 0:
#         start += len(start_str)
#         end = html.find(end, start)
#         if end >= 0:
#             return html[start:end].strip()

api_key = input("请输入您的百度地图API Key: ");
if api_key == '':
    api_key = 'jSVkiBOGSsNh69VzlhaHReHVuZvWvzNA'; # 作者自用API Key，请勿滥用

## 查询根目录下所有csv文件
list = glob.glob('*.csv');
list.remove('main.csv'); # 排除主文件，只定位游记

## 构建json结构
json_file = open(r'data.txt', 'w');

for file_name in list:
    with open(file_name, "r", encoding="utf-8") as csvfile:
        # 读取csv文件，返回的是迭代类型
        print("读取", file_name,"中......")
        read = csv.reader(csvfile);
        for i in read:
            ## 调用百度API
            # url = "http://api.map.baidu.com/geocoder/v2/?ak="+api_key+"&location="+i[0]+","+i[1]+"&output=json&pois=1"
            # req = urllib.request.Request(url)
            # res_data = urllib.request.urlopen(req)
            # res = res_data.read()
            # loaction = txt_wrap_by("\"formatted_address\":\"", "\",\"business\":\"", res.decode("utf-8"))
            # print(loaction)
            str_temp = '{"lat":' + str(i[0]) + ',"lng":' + str(i[1]) + ',"count":1},';
            # 写入json数据
            json_file.write(str_temp)
json_file.close();

## 删除迭代产生的最后一位字符
file_operation = open('data.txt', 'rb+');
file_operation.seek(-1, 2);
file_operation.truncate();
file_operation.seek(0, 0);
file_operation.close();

## 获取json格式的数据内容
json_file = open('data.txt', 'r', encoding='utf8');
json_str = json_file.read();
json_file.close();

## 获取html模板
baiduMap_file = open('baiduMap.html', 'r', encoding='utf8');
baiduHotMap_file = open('baiduHotMap.html', 'r', encoding='utf8');
map_content = baiduMap_file.read();
hotmap_content = baiduHotMap_file.read();
baiduMap_file.close();
baiduHotMap_file.close();

## 生成准备替换的字符串
str = 'var points = ['+json_str+'];';
api_key = 'http://api.map.baidu.com/api?v=2.0&ak='+api_key;

## 注入数据，替换api_key
map_content = map_content.replace('var points = [];', str).replace('http://api.map.baidu.com/api?v=2.0&ak=', api_key);
hotmap_content = hotmap_content.replace('var points = [];', str).replace('http://api.map.baidu.com/api?v=2.0&ak=', api_key);

## 另存为可以使用的html文件
baiduMap_file_copy = open('baiduMap_copy.html', 'w', encoding='utf8');
baiduHotMap_file_copy = open('baiduHotMap_copy.html', 'w', encoding='utf8');
baiduMap_file_copy.write(map_content);
baiduHotMap_file_copy.write(hotmap_content);
baiduMap_file_copy.close();
baiduHotMap_file_copy.close();









