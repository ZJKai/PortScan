from aip import AipOcr
import time

APP_ID = '11524643'
API_KEY = 'Yy2HZg1rgQS9TuWjlgDc9WQY'
SECRET_KEY = 'EOycxwEXhfV6GpMqTsSpELG8TfIcSZQh'

image_path = './image/img2.jpg'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

image = get_file_content(image_path)

""" 如果有可选参数 """
options = {}


result = client.handwriting(image, options)
print(result)