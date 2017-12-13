import os
from PIL import Image

source_folder = '../images/full'
destination_folder = '../images/des'

is_destination_folder_exists = os.path.exists(destination_folder)
if not is_destination_folder_exists:
    os.makedirs(destination_folder)

source_folder_dirs = os.listdir(source_folder)

for filename in source_folder_dirs:
    # 图片转换成128 * 128 灰度图片 
    Image.open(source_folder + '/' + filename).resize((128, 128)).convert('L').save(destination_folder + '/' + filename)
    print(filename)