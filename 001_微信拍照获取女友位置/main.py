# -*-coding:utf-8 -*-

"""
@version: v1.0
@author: Felix
@software: PyCharm
@time: 2019-07-07 19:50
"""

import exifread
import datetime
import transfer
import requests
import json

class Address():

    def __init__(self, img_path):
        self.img_path = img_path
        # 获取坐标的网址和Web服务应用的key
        self.url_get_position = 'https://restapi.amap.com/v3/geocode/regeo?key={}&location={}'
        self.key = "84186b7ed672e00ac924b29ce6f7cfd6"


    # 原始图片提取经纬度信息
    def get_img_exif(self):
        # 导入打开图片，获取原始数据
        with open(self.img_path, 'rb') as f:
            img_exif = exifread.process_file(f)

        # 原图才能读取到属性，进行判断
        if img_exif:
            try:
                # 经度数
                self.longitude_gps = img_exif['GPS GPSLongitude']
                # E,W 东西经方向
                self.longitude_direction = img_exif['GPS GPSLongitudeRef']
                # 纬度数
                self.latitude_gps = img_exif['GPS GPSLatitude']
                # N,S 南北纬方向
                self.latitude_direction = img_exif['GPS GPSLatitudeRef']
                # 拍摄时间
                take_time = img_exif['EXIF DateTimeOriginal']

                is_lie = self.time_is_today(take_time)
                if is_lie:
                    print('很遗憾的通知你，你女朋友发的照片不是今天所拍！！！')
            except:
                print('图片中没有GPS信息')

        else:
            print('图片不是原图')
            return


    # 获取转换后的经纬度坐标
    def get_gps_address(self):
        # 注意，此方法需要使用get_img_exif()中的属性
        # 该get_img_exif()方法要被执行后，属性才能被激活，然后下面被调用
        self.get_img_exif()

        # 原始图片获取的坐标：[103, 45, 54931/1000] <class 'exifread.classes.IfdTag'>
        # 转换后坐标：103.765259, 29.206260
        try:
            lng = self.format_data(self.longitude_gps)
            lat = self.format_data(self.latitude_gps)

            # 经纬度信息完整才进行转换
            if lng and lat:
                # 坐标转换为火星系坐标
                tr = transfer.Transfer()
                location = tr.wg84_to_gcj02(lng, lat)
                gps_address =  f'{location[0]}, {location[1]}'
                return gps_address # (103.76745380953696,29.20330918425425)
            else:
                print(f'图片的数据属性缺失')
                return ''

        # 上面已经打印过没有gps数据，此处跳过
        except:
            pass


    # 判断拍摄时间是否在今天
    def time_is_today(self, take_time):
        # 拍摄时间 2017:09:24 14:30:30
        format_time = str(take_time).split(" ")[0].replace(":", "-")
        # 当天日期, 2017-09-24
        today = str(datetime.date.today())
        if format_time == today:
            return False
        else:
            return True


    # 坐标格式化，转换为小数点6位的浮点数
    def format_data(self, data):
        # 删除左右括号，最后以逗号分隔为一个列表
        data_list_tmp = str(data).replace('[', '').replace(']', '').split(',')
        # 循环取出每个元素，删除元素两边的空格，得到一个新列表
        data_list = [data.strip() for data in data_list_tmp]
        # ['103', '45', '54.931']

        # 替换秒的值
        data_tmp = data_list[-1].split('/')
        # 秒的值
        data_sec = int(data_tmp[0]) / int(data_tmp[1]) / 3600
        # 分的值
        data_minute = int(data_list[1]) / 60
        # 度的值
        data_degree = int(data_list[0])

        # 由于高德API只能识别到小数点后的6位，需要转换为浮点数，并保留为6位小数
        result = "%.6f" % (data_degree + data_minute + data_sec)
        return float(result)


    # 通过高德地图逆向坐标获取地址
    def get_address(self, gps_address):
        # 字符串格式化传入key和location坐标位置(元组格式)，请求获取地址
        resp = requests.get(self.url_get_position.format(self.key, gps_address))
        # 取出地址
        location_data = json.loads(resp.text)
        address = location_data.get('regeocode').get('formatted_address')

        return address


    # 取出经纬度坐标和地址
    def run(self):
        # 提取gps经纬度地址
        gps_address = self.get_gps_address()
        print('图片的经纬度是:(%s)' % gps_address)

        if not gps_address:
            return

        # 根据经度和纬度，获取到详细地址
        address = self.get_address(gps_address)
        print('你女朋友拍照的位置在: %s' % address)


# 使用picture中001图片进行测试
if __name__ == '__main__':
    img_path = './picture/001.jpg'
    address = Address(img_path)
    address.run()