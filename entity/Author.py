class Author:
    def __init__(self, author_data):
        self.author_id = author_data.get("author", {}).get("mthid", None)
        self.author_name = author_data.get("author", {}).get("author", None)
        self.author_icon = author_data.get("author", {}).get("author_icon", None)
        self.authentication_content = author_data.get("author", {}).get("authentication_content", None)
        self.vip_status = author_data.get("author", {}).get("vip", None)
        self.fans_count = author_data.get("cnt", {}).get("fansCnt", None)
        self.fans_count_text = author_data.get("cnt", {}).get("fansCntText", None)
        self.video_count = author_data.get("cnt", {}).get("videoCount", None)
        self.video_count_text = author_data.get("cnt", {}).get("videoCntText", None)
        self.total_play_count = author_data.get("cnt", {}).get("totalPlaycnt", None)
        self.total_play_count_text = author_data.get("cnt", {}).get("totalPlaycntText", None)

    def __repr__(self):
        return f"Author(id={self.author_id}, name={self.author_name}, fans={self.fans_count}, videos={self.video_count})"

    def get_author_details(self):
        details = {
            "author_id": self.author_id,  # 账号id
            "author_name": self.author_name,  # 账号名称
            # "author_icon": self.author_icon,
            # "authentication_content": self.authentication_content,
            "vip_status": self.vip_status,  # 认证信息
            "fans_count": self.fans_count,  # 粉丝数
            "video_count": self.video_count,  # 视频数
        }
        return {k: v for k, v in details.items() if v is not None}
