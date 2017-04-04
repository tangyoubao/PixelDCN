import numpy as np
import h5py
from PIL import Image

# BGR: (104.00698793,116.66876762,122.67891434)
IMG_MEAN = np.array(
    (122.67891434, 116.66876762, 104.00698793), dtype=np.float32)  # RGB


def read_images(data_list):
    with open(data_list, 'r') as f:
        data = [line.strip("\n").split(' ') for line in f]
    return data


def process_image(image, shape, resize_mode=Image.BILINEAR):
    img = Image.open(image)
    img = img.resize(shape, resize_mode)
    img.load()
    return np.asarray(img, dtype="float32")


def build_h5_dataset(data_dir, list_path, out_dir, shape, name, norm=False):
    images = read_images(list_path)
    images_size = len(images)
    dataset = h5py.File(out_dir+name+'.h5', 'w')
    dataset.create_dataset('X', (images_size, *shape, 3), dtype='f')
    dataset.create_dataset('Y', (images_size, *shape), dtype='f')
    for index, (image, label) in enumerate(images):
        if index % 100 == 0:
            print("Dealing ", name, index, images_size)
        image = process_image(data_dir+image, shape)
        label = process_image(data_dir+label, shape, Image.NEAREST)
        image -= IMG_MEAN
        image = image / 255. if norm else image
        dataset['X'][index], dataset['Y'][index] = image, label
    dataset.close()


if __name__ == '__main__':
    shape = (256, 256)
    data_dir = '/tempspace/hyuan/DrSleep/VOC2012/VOCdevkit/VOC2012'
    list_dir = '/tempspace/hyuan/DrSleep/VOC2012/VOCdevkit/VOC2012/dataset/'
    output_dir = '/tempspace/hyuan/DrSleep/VOC2012/VOCdevkit/VOC2012/dataset/'

    data_files = {
        'training': 'train.txt',
        'validation': 'val.txt',
        'testing': 'test.txt'
    }
    for name, list_path in data_files.items():
        build_h5_dataset(data_dir, list_dir+list_path, output_dir, shape, name)
