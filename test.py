from model import  OcrHandle
import base64
from PIL import Image, ImageDraw,ImageFont
from io import BytesIO

import json
import os

from backend.tools.np_encoder import NpEncoder
from backend.tools import log

import logging

logger = logging.getLogger(log.LOGGER_ROOT_NAME + '.' +__name__)

ocrhandle = OcrHandle()

from config import max_post_time ,dbnet_max_size,white_ips

import TextFilter

   
if __name__ == "__main__":
    '''
    :return:
    报错：
    400 没有请求参数
    '''
    cli = TextFilter.CLI()
    short_size = 960
    imgs = os.listdir('imgs/')
    for img_up in imgs:
        print('当前识别的图片：{}'.format(img_up))
        img = Image.open('imgs/' + img_up)
        if hasattr(img, '_getexif') and img._getexif() is not None:
            orientation = 274
            exif = dict(img._getexif().items())
            if orientation not in exif:
                exif[orientation] = 0
            if exif[orientation] == 3:
                img = img.rotate(180, expand=True)
            elif exif[orientation] == 6:
                img = img.rotate(270, expand=True)
            elif exif[orientation] == 8:
                img = img.rotate(90, expand=True)
        
        img = img.convert("RGB")
        

        '''
        是否开启图片压缩
        默认为960px
        值为 0 时表示不开启压缩
        非 0 时则压缩到该值的大小
        '''
        res = []
        do_det = True
        compress_size = 960
        if compress_size is not None:
            try:
                compress_size = int(compress_size)
            except ValueError as ex:
                # logger.error(exc_info=True)
                res.append("短边尺寸参数类型有误，只能是int类型")
                do_det = False
                # self.finish(json.dumps({'code': 400, 'msg': 'compress参数类型有误，只能是int类型'}, cls=NpEncoder))
                # return

            short_size = compress_size
            if short_size < 64:
                res.append("短边尺寸过小，请调整短边尺寸")
                do_det = False

            short_size = 32 * (short_size//32)


        img_w, img_h = img.size
        if max(img_w, img_h) * (short_size * 1.0 / min(img_w, img_h)) > dbnet_max_size:
            # logger.error(exc_info=True)
            res.append("图片reize后长边过长，请调整短边尺寸")
            do_det = False
            # self.finish(json.dumps({'code': 400, 'msg': '图片reize后长边过长，请调整短边尺寸'}, cls=NpEncoder))
            # return


        if do_det:

            res = ocrhandle.text_predict(img,short_size)
            ans = []
            for j in res:
                j = j[1] 
                print(j)
                ans.append(j)
            # print(ans)
            
            cli.default(" ".join(ans))
            print('\n')

            # img_detected = img.copy()
            # img_draw = ImageDraw.Draw(img_detected)
            # colors = ['red', 'green', 'blue', "purple"]

            # for i, r in enumerate(res):
            #     rect, txt, confidence = r

            #     x1,y1,x2,y2,x3,y3,x4,y4 = rect.reshape(-1)
            #     size = max(min(x2-x1,y3-y2) // 2 , 20 )

            #     myfont = ImageFont.truetype("仿宋_GB2312.ttf", size=size)
            #     fillcolor = colors[i % len(colors)]
            #     img_draw.text((x1, y1 - size ), str(i+1), font=myfont, fill=fillcolor)
            #     for xy in [(x1, y1, x2, y2), (x2, y2, x3, y3 ), (x3 , y3 , x4, y4), (x4, y4, x1, y1)]:
            #         img_draw.line(xy=xy, fill=colors[i % len(colors)], width=2)

            # output_buffer = BytesIO()
            # img_detected.save(output_buffer, format='JPEG')
            # byte_data = output_buffer.getvalue()
            # img_detected_b64 = base64.b64encode(byte_data).decode('utf8')
        else:
            output_buffer = BytesIO()
            img.save(output_buffer, format='JPEG') 
            byte_data = output_buffer.getvalue()
            img_detected_b64 = base64.b64encode(byte_data).decode('utf8')
        # return