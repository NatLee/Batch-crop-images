
import argparse
from random import choice
from pathlib import Path

class Option():

    def __init__(self, exts=['.jpg', '.png', '.jpeg']):

        self.__exts = exts

        self.__parser = argparse.ArgumentParser()
        self.__parser.add_argument('--input_path', type=str, default='./img/input', help='Input data path.')
        self.__parser.add_argument('--output_path', type=str, default='./img/result', help='Output data path.')

        self.__opt = self.__parser.parse_args()

        self.input_path = Path(self.__opt.input_path)
        self.output_path = Path(self.__opt.output_path)

        self.check_output_dir()

        self.img_paths = self.get_img_paths()

    def get_img_paths(self):
        return [img for img in self.input_path.glob('*') if img.suffix in self.__exts]

    def check_output_dir(self):
        path = self.output_path
        if not path.is_dir():
            path.mkdir()

    def get_random_one(self):
        return choice(self.img_paths)

    def get_first_one(self):
        return self.img_paths[0]