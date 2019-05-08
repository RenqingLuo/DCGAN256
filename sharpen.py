from PIL import Image, ImageFilter
from glob2 import glob

for fn in glob('faces/*.png'): 
    image = Image.open(fn)
# 打开指定路径的jpg图像文件
    image = image.filter(ImageFilter.SHARPEN)
#锐化滤镜
    splitName=fn.split(".")
    newName=splitName[0]
    image.save(newName+'sharpen.png','png')