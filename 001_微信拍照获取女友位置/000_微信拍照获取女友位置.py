# -*-coding:utf-8 -*-

import exifread
import datetime
import transfer
import requests
import json

img_path = './001_test.jpg'


def get_img_exif():
    # 导入原始图片，获取原始数据
    img_exif = exifread.process_file(open(img_path, 'rb'))

    # 如果是原图才能读取到属性
    if img_exif:
        # 经度数
        global longitude_gps
        longitude_gps = img_exif['GPS GPSLongitude']
        print(longitude_gps)

        # E,W 东西经方向
        longitude_direction = img_exif['GPS GPSLongitudeRef']

        # 纬度数
        global latitude_gps
        latitude_gps = img_exif['GPS GPSLatitude']
        print(latitude_gps)

        # N,S 南北纬方向
        latitude_direction = img_exif['GPS GPSLatitudeRef']

        # 拍摄时间
        global take_time
        take_time = img_exif['EXIF DateTimeOriginal']
        print(take_time)


# 判断拍摄时间是否在今天
def time_is_today():
    # 拍摄时间 2017:09:24 14:30:30
    format_time = str(take_time).split(" ")[0].replace(":", "-")

    # 当天日期, 2017-09-24
    today = str(datetime.date.today())

    if format_time == today:
        return False
    else:
        return True


get_img_exif()
time_is_today()
lng = longitude_gps # [103, 45, 54931/1000] <class 'exifread.classes.IfdTag'>
lat = latitude_gps # [29, 12, 225373/10000]
print(type(lng))
print(type(lat))
print(str(lng))
print(type(str(lng)))


def __format_lati_long_data(self, data):
    """
    对经度和纬度数据做处理，保留6位小数
    :param data: 原始经度和纬度值
    :return:
    """
    # 删除左右括号，最后以逗号分隔为一个列表
    data_list_tmp = str(data).replace('[', '').replace(']', '').split(',')
    # 循环取出每个元素，删除元素两边的空格，得到一个新列表
    data_list = [data.strip() for data in data_list_tmp]
    # ['103', '45', '54.931']

    # 替换秒的值
    data_tmp = data_list[-1].split('/')

    # 秒的值
    data_sec = int(data_tmp[0]) / int(data_tmp[1]) / 3600

    # 替换分的值
    data_tmp = data_list[-2]

    # 分的值
    data_minute = int(data_tmp) / 60

    # 度的值
    data_degree = int(data_list[0])

    # 由于高德API只能识别到小数点后的6位
    # 需要转换为浮点数，并保留为6位小数
    result = "%.6f" % (data_degree + data_minute + data_sec)
    return float(result)


def __get_address(self, location):
    """
    根据坐标得到详细地址
    :param location: 经纬度值
    :return:
    """
    resp = requests.get(self.url_get_position.format(self.api_key, location))

    location_data = json.loads(resp.text)

    address = location_data.get('regeocode').get('formatted_address')

    return address


print()

# tr = transfer.Transfer()
# print(tr.bd09_to_gcj02(lng, lat))








