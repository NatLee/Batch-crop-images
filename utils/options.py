import argparse
from pathlib import Path

class Options():
    def __init__(self):
        self.__parser = argparse.ArgumentParser()
        self.__parser.add_argument('--input_path', type=str, default='./img/input', help='Input data path.')
        self.__parser.add_argument('--output_path', type=str, default='./img/result', help='Output data path.')
        self.__opt = self.__parser.parse_args()

        self.input_path = Path(self.__opt.input_path)
        self.output_path = Path(self.__opt.output_path)
        self.checkOutDir()

    def checkOutDir(self):
        path = self.output_path
        if not path.is_dir():
            path.mkdir()