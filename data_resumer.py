import csv
import os
import pickle
import time

import config
import gbl
from csv_process import CsvHandler

class DataResumer:
    def __init__(self, filepath='gbl.pkl'):
        self.filepath = filepath
        self.state = {
            'visited_author_map': gbl.visited_author_map,
            'video_counter': gbl.video_counter,
            'comment_counter': gbl.comment_counter
        }
        # 尝试加载之前的状态
        self.load_state()

    def save_state(self):
        """将当前状态保存到文件"""
        try:
            # 获取 last_author_id
            last_author_id = gbl.last_author_id

            if last_author_id:
                # 删除 last_author 的所有数据

                # 1. 删除 author.csv 列 author_id 为 last_author_id 的行
                author_csv_file = config.author_dir + 'author.csv'  # 假设文件名为 author.csv
                self.remove_author_data(author_csv_file, last_author_id)

                # 2. 删除该作者的视频信息文件 author_id_video.csv
                video_csv_file = f"{config.video_dir}{last_author_id}_video.csv"  # 假设视频信息的文件名为 author_id_video.csv
                self.remove_file(video_csv_file)
                print(f"已删除视频 {last_author_id}_video.csv")
                # 3. 删除该作者的视频评论信息目录
                comment_dir = f"{config.comment_dir}{last_author_id}"  # 假设评论文件夹路径为 /data/comment/last_author_id
                print(f"已删除评论 {comment_dir}")
                self.remove_directory(comment_dir)
                # 刷新全局状态
                # 删除last_author_id key
                gbl.video_counter = max(0, gbl.video_counter - gbl.visited_author_map[last_author_id])
                del gbl.visited_author_map[last_author_id]
                self.state = {
                    'visited_author_map': gbl.visited_author_map,
                    'video_counter': gbl.video_counter,
                    'comment_counter': gbl.comment_counter
                }
            # 最后保存当前状态
            with open(self.filepath, 'wb') as f:
                pickle.dump(self.state, f)
            print("状态已保存。")
        except Exception as e:
            print(f"保存状态时发生错误: {e}")

    def remove_author_data(self, author_csv_file, author_id):
        """删除 author.csv 中 author_id 为指定作者的行"""
        try:
            if os.path.exists(author_csv_file):
                # 读取原始数据并删除指定行
                with open(author_csv_file, 'r', newline='', encoding='utf-8') as infile:
                    reader = csv.reader(infile)
                    rows = list(reader)

                # 找到并删除指定作者的数据
                rows = [row for row in rows if row[0] != author_id]  # 假设 author_id 在第一列

                # 写回文件
                with open(author_csv_file, 'w', newline='', encoding='utf-8') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerows(rows)
                print(f"已从 {author_csv_file} 中删除 author_id 为 {author_id} 的数据。")
        except Exception as e:
            print(f"删除 author 数据时发生错误: {e}")

    def remove_file(self, file_path):
        """删除指定的文件"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"已删除文件: {file_path}")
        except Exception as e:
            print(f"删除文件时发生错误: {e}")

    def remove_directory(self, dir_path):
        """删除指定的目录及其内容"""
        try:
            if os.path.exists(dir_path):
                # 删除目录中的所有文件
                for filename in os.listdir(dir_path):
                    file_path = os.path.join(dir_path, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                # 删除空目录
                os.rmdir(dir_path)
                print(f"已删除目录及其内容: {dir_path}")
        except Exception as e:
            print(f"删除目录时发生错误: {e}")

    def load_state(self):
        """从文件加载之前保存的状态"""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'rb') as f:
                    self.state = pickle.load(f)
                gbl.visited_author_map = self.state['visited_author_map']
                gbl.video_counter = self.state['video_counter']
                gbl.comment_counter = self.state['comment_counter']
                print(f'map大小为{len(gbl.visited_author_map)}, 视频计数器为{gbl.video_counter}, 评论计数器为{gbl.comment_counter}')
                print("状态已恢复。")
            except Exception as e:
                print(f"加载状态时发生错误: {e}")
        else:
            print("没有找到之前的状态，初始化为默认状态。")