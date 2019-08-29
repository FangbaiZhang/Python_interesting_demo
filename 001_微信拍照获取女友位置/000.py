

# data = "[103, 45, 54931/1000]"

# 纬度
data = "[29, 12, 225373/10000]"

# 获取的原始经纬度，格式为类似一个列表，三个数字分别代表[度，分，秒]
# 原始经纬度类型：<class 'exifread.classes.IfdTag'>，转换为字符串
# 删除两边括号，逗号分隔为列表，在删除每个元素两边的空格
data_list_tmp = str(data).replace('[', '').replace(']', '').split(',')
data_list = [data.strip() for data in data_list_tmp]
print(data_list)

# 秒的值分子分母进行分割
data_tmp = data_list[-1].split('/')

# 秒转换为度，秒的值除以3600
data_sec = int(data_tmp[0]) / int(data_tmp[1]) / 3600

# 分转换为度，分的值除以60
data_minute = int(data_list[-2]) / 60

# 度的值
data_degree = int(data_list[0])

# 由于高德API只能识别到小数点后的6位
# 需要转换为浮点数，并保留为6位小数
result = "%.6f" % (data_degree + data_minute + data_sec)

# 29.20626

print(float(result))