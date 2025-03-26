import os
import random
import time
import traceback

import gbl
from comment_spider import CommentSpider
from csv_process import CsvHandler
from data_collection import DataCollection
from config import *
from data_resumer import DataResumer

class Business:
    def __init__(self):
        self.data_resumer = DataResumer()

    def letsGo(self, comment_counter=None):
        # 初始化数据收集器
        data_collection = DataCollection(max_one_user_video_nums=max_one_user_video_nums,
                                         max_author_nums=total_author_nums)

        total_authors = total_author_nums  # 总作者数
        # 最近一次评论数
        c = 0
        # 记录开始时间
        start_time = time.time()
        try:
            while True:
                # 每次循环开始时记录当前时间
                loop_start_time = time.time()
                # 从feed流获得一个作者
                account = data_collection.get_one_account_by_feed()
                if account is None:
                    break
                # 处理当前作者

                # 初始化csv处理器
                author_acv_handler = CsvHandler(csv_directory=author_dir, csv_file_name='author')
                # 保存作者信息
                author_acv_handler.save_data(account.get_author_details())

                gbl.last_author_id = account.author_id
                # 获取一批视频列表
                video_list = data_collection.get_all_video_list(author=account)
                v_info_list = []

                for i in video_list:
                    t = data_collection.video_on_author_parser(i["content"]["vid"], i["content"]["duration"]                               , account)
                    if t is None:
                        continue
                    v_info_list.append(t.get_video_details())
                    slp = random.randint(1, 2)
                    print(f"sleep {slp} seconds -html")
                    time.sleep(slp)
                # 保存视频信息
                video_csv_handler = CsvHandler(csv_directory=video_dir, csv_file_name=account.author_id + "_video")
                video_csv_handler.save_data(v_info_list)

                for i in v_info_list:
                    comment_spider = CommentSpider(max_one_comment_nums=max_one_comment_nums,
                                                   author_id=account.author_id, v_json=i)
                    comment_list = comment_spider.get_all_comments_by_vid()
                    comment_csv_handler = CsvHandler(csv_directory=comment_dir+account.author_id+'/', csv_file_name=i["id"] + "_comment")
                    gbl.comment_counter += len(comment_list)
                    c = len(comment_list)
                    comment_csv_handler.save_data(comment_list)
                # 计算并打印每个循环的已用时间和预计剩余时间
                loop_end_time = time.time()
                loop_duration = loop_end_time - loop_start_time
                avg_time_per_author = (loop_end_time - start_time) / len(gbl.visited_author_map)  # 每个作者平均耗时
                remaining_authors = total_authors - len(gbl.visited_author_map)
                estimated_remaining_time = remaining_authors * avg_time_per_author
                # 打印当前的已用时间、预计剩余时间、当前进度
                elapsed_time = loop_end_time - start_time
                print(f"已处理作者 {gbl.visited_author_map}/{total_authors}，已用时间: {elapsed_time:.2f}秒，预计剩余时间: {estimated_remaining_time:.2f}秒")

        except KeyboardInterrupt:
            # 捕获键盘中断并保存状态
            print("程序被用户中断，正在保存数据...")
            gbl.comment_counter -= c
            self.data_resumer.save_state()

        except Exception as e:
            # 捕获其他异常并保存状态
            print(f"发生异常: {e}，正在保存数据...")

            # 打印堆栈信息
            traceback.print_exc()  # 打印完整的堆栈信息

            # 如果需要将堆栈信息作为字符串保存
            stack_trace = traceback.format_exc()
            print(f"异常堆栈信息：\n{stack_trace}")
            self.data_resumer.save_state()

        finally:
            print(
                f"all done, 作者总数: {len(gbl.visited_author_map)}, 视频总数: {gbl.video_counter}, 评论总数: {comment_counter}")
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            print(f"all done, 作者总数: {len(gbl.visited_author_map)},视频总数: {gbl.video_counter}, 评论总数: {gbl.comment_counter}")


    # if __name__ == '__main__':
#     b = Business()
#     b.letsGo()
