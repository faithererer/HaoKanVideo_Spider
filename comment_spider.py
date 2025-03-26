import random
import time

from gbl import *
from api import *


class CommentSpider:
    def __init__(self, max_one_comment_nums, author_id, v_json):
        self.max_one_comment_nums = max_one_comment_nums
        self.author_id = author_id
        self.v_id = v_json.get("id")
        self.v_json = v_json

    def get_all_comments_by_vid(self):
        """
        根据视频id获取全部评论(限制范围内)
        :param video_id:
        :return:
        """
        r = []
        comment_list = []
        # 获取评论
        print(self.v_json)
        total_comment_num = min(self.max_one_comment_nums, self.v_json.get("comment_count"))
        print("total_comment_num:", total_comment_num)
        maxPn = total_comment_num // 20 + 1
        for pn in range(1, maxPn+1):
            res = session.get(COMMENT_LIST, headers=headers,
                              params={
                                  'rn': 20,
                                  'pn': pn,
                                  'url_key': self.v_id,
                              })
            raw = res.json()['data']["list"]
            from entity.Comment import Comment
            for i in raw:
                comment = Comment(i)
                r.append(comment.get_comment_details())
            print(f"评论区进度【{pn}/{maxPn}】")
            time.sleep(1)
        return r


# if __name__ == '__main__':
#     print(CommentSpider(max_one_comment_nums=10, author_id=1, v_id=5650068575566295516).get_all_comments_by_vid()
#           )

