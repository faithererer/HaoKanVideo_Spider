import codecs
import json
import os

import pandas
import pandas as pd


class CsvHandler:
    def __init__(self, csv_directory, csv_file_name):
        self.csv_directory = csv_directory
        self.csv_file_name = csv_file_name

    def save_data(self, json_data):
        # 检测文件夹
        if not os.path.exists(self.csv_directory):
            os.makedirs(self.csv_directory)

        # 如果json_data是一个字典，将其包装成列表
        if isinstance(json_data, dict):
            json_data = [json_data]  # 将字典包装成一个包含字典的列表

        # 保存数据，追加写，使用pandas
        file_path = "%s%s.csv" % (self.csv_directory, self.csv_file_name)

        # 如果文件不存在，写入表头
        if not os.path.exists(file_path):
            header = True
        else:
            header = False

        # 使用pandas保存数据
        pd.DataFrame(json_data).to_csv(
            file_path,
            index=False,
            mode='a',
            encoding='utf-8-sig',
            header=header
        )
        print(f"saved data to {file_path}")

    def remove_csv(self):
        file_path = "%s%s.csv" % (self.csv_directory, self.csv_file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"removed csv file {file_path}")
        else:
            print(f"csv file {file_path} does not exist")
