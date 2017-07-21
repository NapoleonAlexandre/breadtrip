# coding=utf-8

## Author: Jiahao Wang (Frank)
#  Date: 2017.7
#  Email: sb418723601@gmail.com
#  Info: 此脚本为基于WebDriver的面包旅行（breadtrip.com）网页爬虫，请更改browser.get()括号内的链接前往其他城市

## 引入WebDriver包
from selenium import webdriver
import time
import random
import csv
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

## 取得具体游记的坐标信息并且储存为csv文件
def getDetailedLocation(url):

    print("等待网页加载完毕......");

    ## 导航到具体网页
    browser_sub.get(url);
    browser_sub.implicitly_wait(10);

    print("......加载完毕，开始解析内容并构建数据库");

    link_name = url.split('/');
    file_name = link_name[-2]+'.csv';
    with open(file_name, 'w', newline='') as sub_file:
        writer = csv.writer(sub_file, dialect='excel');

        ## 寻找地图信息
        # map: list[]
        map = browser_sub.find_element_by_id('map_data');
        # map_data: all the data under the id of “map_data”
        map_data = map.find_elements_by_xpath("*");
        for element in map_data:
            print("--------------------------------");

            #location is a list, having two elements
            location = element.find_elements_by_tag_name('span');
            location_type = str(element.get_attribute('data-type'));

            ## 通过innerHTML解析隐藏内容
            location_lat = str(location[0].get_attribute('innerHTML'));
            location_lng = str(location[1].get_attribute('innerHTML'));

            ## 输出坐标
            print("坐标：", location_lat, ", ", location_lng);
            print("坐标类型：", location_type);

            writer.writerow([location_lat, location_lng, location_type]);

        sub_file.close();

    print("--------------------------------");

    return 0;

## 获取Firefox配置文件对象
firefoxProfile = FirefoxProfile();
## 禁用CSS
firefoxProfile.set_preference('permissions.default.stylesheet', 2);
## 禁用图像
firefoxProfile.set_preference('permissions.default.image', 2 );
## 禁用Flash
firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false');

## 创建浏览器对象
browser = webdriver.Firefox(firefoxProfile, executable_path="/Users/ychern/Desktop/breadtrip_research_in_FuDanUniversity-master/geckodriver");

## 导航到面包旅行昭通
browser.get('http://web.breadtrip.com/scenic/3/61123/trip/#nav');

print("等待网页加载完毕......");

## 检查标题是否为‘昭通-目的地-面包旅行’
assert '昭通-目的地-面包旅行' in browser.title;

## 创建循环直到加载所有旅行信息
while True:
    # 寻找“加载更多”按钮
    elem = browser.find_element_by_id('load-more');
    # 如果尚有未加载内容
    travel_style = elem.get_attribute("style");
    if travel_style  == "display: block;":
        # 在一个随机的时间后触发点击事件
        time_gap = random.randrange(1,4,1);
        print("自动加载未展开内容，下次加载在", time_gap, "s之后");
        time.sleep(time_gap);
        elem.click();
    elif travel_style  == "display: none;":
        # 加载完毕，结束循环
        print("......加载完毕");
        break;
    else:
        continue;

## 解析网页元素
travel = browser.find_element_by_class_name('single-trip');
travel_list = travel.text.split("\n");
# 取得日志数量
travel_num = int(len(travel_list)/3);
travel_objects = travel.find_elements_by_xpath("*");

## 创建子浏览器对象
browser_sub = webdriver.Firefox(firefoxProfile);

## 建立主数据库文件
with open('main.csv', 'w', newline='') as main_file:
    writer = csv.writer(main_file, dialect='excel');

    for index in range(travel_num):
        print("--------------------------------");
        # 日志作者
        author = str(travel_list[index*3].split("by")[1]);
        travel_info = travel_list[index*3+1].split("：");
        # 旅行时长
        travel_time = str(int(travel_info[1].split("天")[0]));
        # 旅行路径
        travel_path = str(travel_info[2].split(">"));
        # 日志链接
        travel_link = str(travel_objects[index].find_elements_by_xpath("*")[0].get_attribute("href"));
        # 排除过短日志
        if len(travel_path) <= 1:
            print("[过短标记]作者：", author);
            print("[过短标记]旅行时长：", travel_time, "天");
            print("[过短标记]足迹：", travel_path);
            print("[过短标记]链接：", travel_link);
        else:
            print("作者：", author);
            print("旅行时长：", travel_time, "天");
            print("足迹：", travel_path);
            print("链接：", travel_link);
        print("正在写入数据库");
        writer.writerow([author, travel_time, travel_path, travel_link]);
        print("开始解析该日志足迹......");
        getDetailedLocation(travel_link);
        print("......解析完毕");

print("--------------------------------");

main_file.close();

## 关闭浏览器
browser_sub.quit();
browser.quit();