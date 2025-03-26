import random
import re
import time

import pandas as pd

import gbl
from comment_spider import CommentSpider
from config import max_one_user_video_nums, total_author_nums, video_dir, comment_dir, max_one_comment_nums
from csv_process import CsvHandler
from data_collection import DataCollection
from entity.Author import Author


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
    elif re.match(r'([\d.]+)(次播放)', s):
        return re.match(r'([\d.]+)(次播放)', s).group(1)
    else:
        # 没有单位的情况，直接返回整数
        return int(s)

if __name__ == '__main__':
    pass
    # data_collection = DataCollection(max_one_user_video_nums, total_author_nums)
    # # 获取一批视频列表
    # account = Author({
    #     "author": {
    #         "mthid": "ui2af56Gkl8wK3Zh_FPfSA"
    #     }
    # })
    # gbl.visited_author_map[account.author_id] = 0
    #
    # video_list = data_collection.get_all_video_list_fix(author=account)
    # print(account.author_id)
    # v_info_list = []
    # print(video_list)
    # for i in video_list:
    #     t = data_collection.video_on_author_parser(i["content"]["vid"], i["content"]["duration"], account)
    #     if t is None:
    #         continue
    #     v_info_list.append(t.get_video_details())
    #     slp = random.randint(1, 2)
    #     print(f"sleep {slp} seconds -html")
    #     time.sleep(slp)
    # # 保存视频信息
    # video_csv_handler = CsvHandler(csv_directory=video_dir, csv_file_name=account.author_id + "_video")
    # video_csv_handler.remove_csv()
    # video_csv_handler.save_data(v_info_list)
    # print("视频信息保存完成")
    # for i in v_info_list:
    #     comment_spider = CommentSpider(max_one_comment_nums=max_one_comment_nums,
    #                                    author_id=account.author_id, v_json=i)
    #     comment_list = comment_spider.get_all_comments_by_vid()
    #     comment_csv_handler = CsvHandler(csv_directory=comment_dir + account.author_id + '/',
    #                                      csv_file_name=i["id"] + "_comment")
    #     gbl.comment_counter += len(comment_list)
    #     c = len(comment_list)
    #     comment_csv_handler.remove_csv()
    #     comment_csv_handler.save_data(comment_list)
    #

