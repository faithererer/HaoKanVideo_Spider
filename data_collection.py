import codecs
import json
import random
import re
import time
from datetime import datetime

import lxml.etree
import requests
from lxml import etree

import gbl
from entity.Author import Author
from api import *
from config import headers
from entity.Video import Video


class DataCollection:
    """
    收集数据
    """

    def __init__(self, max_one_user_video_nums, max_author_nums):
        self.max_one_user_video_nums = max_one_user_video_nums
        self.max_author_nums = max_author_nums
        self.session = gbl.session


    def convert(self, s):
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

    def video_on_author_parser(self, vid, duration, author):
        # 根据页面内容获取视频信息
        """
     {
            "id": self.id,  # 视频id
            "title": self.title,  # 视频名称
            "duration": self.duration,  # 视频长度
            "like_count": self.like,  # 点赞次数
            "comment_count": self.comment,  # 评论次数
            "play_count": self.playcnt,  # 播放次数
            "publish_time": self.publish_time  # 发布时间
        }
        """
        author_id = author.author_id
        # 判断已经爬取的视频数目是否超出
        if gbl.visited_author_map[author_id] >= self.max_one_user_video_nums:
            return None
        # +1
        gbl.visited_author_map[author_id] += 1
        print(
            f"开始爬取{author_id}的第{gbl.visited_author_map[author_id]}个视频\t状态=>【当前作者数/目标作者数: {len(gbl.visited_author_map)}/{self.max_author_nums}, 当前作者视频/作者总视频数<限制数>: {gbl.visited_author_map[author_id]}/{author.video_count}<{self.max_one_user_video_nums}>, 当前总视频数: {gbl.video_counter}】")
        # 统计
        gbl.video_counter += 1
        video = {
            'id': vid
        }
        htm = requests.get(VEDIO_DETAILS_URL, headers=headers, params={'vid': vid})

        # 解析 HTML
        tree = etree.HTML(htm.text)
        title_path = tree.xpath('//*[@id="rooot"]/div[2]/div[1]/div[3]/text()')
        if title_path in [None, []]:
            print(htm.text)
            # 统计
            gbl.video_counter -= 1
            # +1
            gbl.visited_author_map[author_id] -= 1
            print(
                f"获取视频信息失败, 跳过\t状态=>【当前作者数/目标作者数: {len(gbl.visited_author_map)}/{self.max_author_nums}, 当前作者视频/作者总视频数<限制数>: {len(gbl.visited_author_map)}/{author.video_count}<{self.max_one_user_video_nums}>, 当前总视频数: {gbl.video_counter}")
            return None
        print(title_path[0])
        video['title'] = title_path[0]
        play_cnt_path = tree.xpath('/html/head/meta[14]/@content')[0]
        # 使用正则表达式提取播放量
        play_count_re = re.search(r'(\d+)次播放', play_cnt_path)
        video['play_count'] = self.convert(play_count_re.group(1))
        video['duration'] = duration
        like_path = tree.xpath('//*[@id="rooot"]/div[2]/div[1]/div[2]/div/div[2]/text()')[0]
        video['like_count'] = self.convert(like_path)
        # 包含"万"处理为数字

        comment_path = tree.xpath('//*[@id="rooot"]/div[2]/div[1]/div[2]/div/div[1]/text()')[0]
        video['comment_count'] = comment_path
        publish_time_path = tree.xpath('//*[@id="rooot"]/div[2]/div[1]/div[2]/text()')[0]
        video['publish_time'] = publish_time_path
        # 使用正则表达式提取日期部分
        date_match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', video['publish_time'])

        if date_match:
            # 获取年、月、日部分
            year = date_match.group(1)
            month = date_match.group(2)
            day = date_match.group(3)

            # 将日期转换为 Python datetime 对象
            date_str = f"{year}-{month}-{day}"
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            # 转换为 yy-mm-dd 格式
            formatted_date = date_obj.strftime("%Y-%m-%d")
            video['publish_time'] = formatted_date
            # 作者
            author_detail = self.get_author_by_vid(vid)
            return Video(video, isFeed=False)

    def get_author_by_vid(self, video_id):
        """
        :param video_id:
        :return: Author
        """
        # 判断是否超出
        v_res = self.session.get(AUTHOR_INFO_BY_VIDEO, params={"vid": video_id}, headers=headers)
        author = v_res.json().get("data").get("response")
        return Author(author)

    def get_one_account_by_feed(self):
        """
        从feed流中获取一个账号
        :return: Author
        """
        v_res = self.session.get(VIDEO_LIST_URL_FEED, headers=headers)
        video_list = list(v_res.json().get("data").get("response").get("videos"))
        for item in video_list:
            video = Video(item, isFeed=True)
            # 判断作者是否存在
            if video.mthid in gbl.visited_author_map:
                continue
            # 判断作者总数是否超出
            if len(gbl.visited_author_map) >= self.max_author_nums:
                print("作者总数超出限制, 退出")
                return None
            gbl.visited_author_map[video.mthid] = 0
            author_detail = self.get_author_by_vid(video.id)
            print(f"当前作者: {author_detail.author_id}\t{author_detail.author_name}")
            return author_detail

    def next_video_list(self, author_id, ctime=None):
        res_list = self.session.get(VEDIO_LIST_BY_AUTHOR, headers=headers,
                                    params={
                                        "app_id": author_id,
                                        "ctime": ctime
                                    })
        return res_list.json()

    def get_all_video_list(self, author):
        """
        获取一个作者的所有视频列表,在限制范围内
        new 最新视频播放量太少。尽可能跳过最新视频，跳过前30个
        :param author:
        :return:
        """
        c = 0
        cur_one_user_video_count = 0
        video_list = []
        ctime = None
        # 跳过20个最新视频
        for i in range(2):
            res_list = self.next_video_list(author.author_id, ctime=ctime)
            if res_list['data']['has_more'] == 0:
                ctime = None
                break
            ctime = res_list['data']['ctime']
            c += len(res_list['data']['results'])
            time.sleep(0.5)
        print(f"跳过, {c}个视频，next=>{ctime}")

        while True:
            # 检测单个作者视频数量是否超出
            if cur_one_user_video_count > self.max_one_user_video_nums:
                return video_list
            res_list = self.next_video_list(author.author_id, ctime=ctime)
            if res_list['data']['has_more'] == 0:
                break
            ctime = res_list['data']['ctime']
            t = res_list['data']['results']
            cur_one_user_video_count += len(t)
            for item in t:
                video_list.append(item)
            if res_list['data']['has_more'] == 0:
                break
            time.sleep(1)
        return video_list

    def get_all_video_list_fix(self, author):
        """
        获取一个作者的所有视频列表,在限制范围内
        :param author:
        :return:
        """
        c = 0
        cur_one_user_video_count = 0
        video_list = []
        ctime = None
        while True:
            # 检测单个作者视频数量是否超出
            if cur_one_user_video_count > self.max_one_user_video_nums:
                return video_list
            res_list = self.next_video_list(author.author_id, ctime=ctime)
            print(res_list)
            ctime = res_list['data']['ctime']
            t = res_list['data']['results']
            cur_one_user_video_count += len(t)
            for item in t:
                video_list.append(item)
            if res_list['data']['has_more'] == 0:
                break
            time.sleep(random.randint(1, 2))
        return video_list
