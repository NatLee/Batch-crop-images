import click

import cv2

from utils import Option, Cropper

if __name__ == '__main__':

    opt = Option()
    img_paths = opt.img_paths

    raw_img = cv2.imread(opt.get_first_one().absolute().as_posix())
    cropper = Cropper(raw_img)

    if cropper.cropped:

        start, end = cropper.get_start_end()

        startx, starty = start
        endx, endy = end

        last_size = None

        for img_path in img_paths:

            img = cv2.imread(img_path.absolute().as_posix())

            height, width, _ = img.shape
            size = (width, height)
            if last_size and last_size != size:

                print('[Notice]')
                print(f'Detect size of {img_path} is {size}. It\'s not compatible with first one {last_size}.')
                print('This image will be resized for cropping(original image WON\'T been modified).')
                print('Would you want to continue? [y/n]')

                while True:
                    yn = input().lower()
                    if yn in ['y', 'n', 'yes', 'no']:
                        if yn == 'y' or yn == 'yes':
                            img = cv2.resize(img, last_size)
                            print(f'{img_path} has been resized.')
                            break
                        else:
                            print('Abort.')
                            exit(-1)
                    else:
                        print('Please input [y/n].')

            else:
                last_size = size

            cropped_img = img[starty:endy, startx:endx, :]
            cv2.imwrite((opt.output_path / img_path.name).absolute().as_posix(), cropped_img)
