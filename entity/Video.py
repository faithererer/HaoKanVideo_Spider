class Video:
    def __init__(self, video_data, isFeed=False):
        if isFeed:
            self.id = video_data.get("id")
            self.title = video_data.get("title")
            self.poster = video_data.get("poster")
            self.poster_small = video_data.get("poster_small")
            self.poster_big = video_data.get("poster_big")
            self.poster_pc = video_data.get("poster_pc")
            self.source_name = video_data.get("source_name")
            self.play_url = video_data.get("play_url")
            self.playcnt = video_data.get("playcnt")
            self.mthid = video_data.get("mthid")
            self.mthpic = video_data.get("mthpic", "")
            self.threadId = video_data.get("threadId")
            self.site_name = video_data.get("site_name", "")
            self.duration = video_data.get("duration")
            self.url = video_data.get("url")
            self.cmd = video_data.get("cmd")
            self.loc_id = video_data.get("loc_id")
            self.commentInfo = video_data.get("commentInfo", {})
            self.comment_id = video_data.get("comment_id")
            self.show_tag = video_data.get("show_tag", 0)
            self.publish_time = video_data.get("publish_time")
            self.new_cate_v2 = video_data.get("new_cate_v2")
            self.appid = video_data.get("appid", "")
            self.path = video_data.get("path", "")
            self.channel_name = video_data.get("channel_name", "")
            self.channel_total_number = video_data.get("channel_total_number", 0)
            self.channel_poster = video_data.get("channel_poster", "")
            self.previewUrlHttp = video_data.get("previewUrlHttp")
            self.is_long_video = video_data.get("is_long_video", False)
            self.like = video_data.get("like", 0)
            self.fmlike = video_data.get("fmlike", "0")
            self.comment = video_data.get("comment", "0")
            self.fmcomment = video_data.get("fmcomment", "0")
            self.fmplaycnt = video_data.get("fmplaycnt", "0次播放")
            self.fmplaycnt_2 = video_data.get("fmplaycnt_2", "0")
            self.outstand_tag = video_data.get("outstand_tag", "")
            self.rank = video_data.get("rank", 0)
            self.is_back_haokan = video_data.get("is_back_haokan", 0)
            self.back_haokan_scheme = video_data.get("back_haokan_scheme", "")
            self.third_id = video_data.get("third_id")
            self.author_avatar = video_data.get("author_avatar")
            self.show_type = video_data.get("show_type", 0)
        else:
            self.id = video_data.get("id")
            self.title = video_data.get("title")
            self.duration = video_data.get("duration")
            self.like = video_data.get("like_count")
            self.comment = int(video_data.get("comment_count", 0) or 0)
            self.playcnt = video_data.get("play_count")
            self.publish_time = video_data.get("publish_time")



    def __repr__(self):
        return f"Video(id={self.id}, title={self.title}, playcnt={self.playcnt})"

    def get_video_details(self):
        return {
            "id": self.id,  # 视频id
            "title": self.title,  # 视频名称
            "duration": self.duration,  # 视频长度
            "like_count": self.like,  # 点赞次数
            "comment_count": self.comment,  # 评论次数
            "play_count": self.playcnt,  # 播放次数
            "publish_time": self.publish_time  # 发布时间
        }


    def is_video_long(self):
        return self.is_long_video
