import os
import pickle
import numpy as np

from PIL import Image

source_folder = '../images/full'
destination_folder = '../images/des'
binary_folder = '../images/binary/images.bin'
binary_array = []
is_destination_folder_exists = os.path.exists(destination_folder)
if not is_destination_folder_exists:
    os.makedirs(destination_folder)

source_folder_dirs = os.listdir(source_folder)

for filename in source_folder_dirs:
    # 图片转换成128 * 128 灰度图片 
    l_128 = Image.open(source_folder + '/' + filename).resize((128, 128)).convert('L')
    # 存储生成的图片
    l_128.save(destination_folder + '/' + filename)
    l_128_array = np.array(l_128,'f')
    binary_array.append(l_128_array)
    # 存储
    print(filename)

with open(binary_folder, mode='wb') as f:
    pickle.dump(binary_array, f)