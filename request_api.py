from requests import post
import json
import base64

image_path = r'\\wsl.localhost\Ubuntu-18.04\home\honk\ocr\data\test\imgs\3.jpeg'

def Image2Base64(image_path):
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read())

data={
     'img': Image2Base64(image_path),           #图片数据的Base64编码
      'compress': 0,                           #图片短边的压缩目标像素，防止图像过大。其值应当在(0, 6000)
     }

r = post('http://172.22.43.64:8089/api/tr-run/', data=data)
# print(r.text)
print(json.loads(r.text))