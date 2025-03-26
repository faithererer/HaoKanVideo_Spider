import requests

import config
from config import *
session = requests.Session()
# session.proxies = config.proxies
# <author_id, video_nums>
visited_author_map = {}
# 视频计数器
video_counter = 0
# 评论计数器
comment_counter = 0

last_author_id = None
