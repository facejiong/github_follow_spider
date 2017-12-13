import pickle

binary_folder = '../images/binary/images.bin'

print(pickle.load(open(binary_folder, 'rb')))