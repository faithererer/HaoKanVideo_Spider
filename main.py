import re

from business import Business
from comment_spider import CommentSpider
from config import video_dir, max_one_comment_nums, comment_dir, total_author_nums, max_one_user_video_nums, author_dir
from csv_process import CsvHandler
from data_collection import DataCollection


def convert( s):
    # 处理"万"和"亿"
    match = re.match(r'([\d.]+)(万|亿)', s)
    if match:
        number = float(match.group(1))
        unit = match.group(2)
        if unit == '万':
            return int(number * 10000)  # 乘以10000后转换为整数
        elif unit == '亿':
            return int(number * 100000000)  # 乘以100000000后转换为整数
    else:
        # 没有单位的情况，直接返回整数
        return int(s)
if __name__ == '__main__':
    b = Business()
    b.letsGo()

