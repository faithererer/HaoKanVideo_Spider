
class Comment:
    def __init__(self, comment_data):
        # 基本评论信息
        self.comment_id = comment_data.get("reply_id", None)
        self.author_name = comment_data.get("uname", None)
        self.avatar = comment_data.get("avatar", None)
        self.content = comment_data.get("content", None)
        self.create_time = comment_data.get("create_time", None)
        self.create_time_text = comment_data.get("create_time_text", None)
        self.like_count = comment_data.get("like_count", 0)
        self.reply_count = comment_data.get("reply_count", 0)
        self.is_anonymous = comment_data.get("is_anonymous", 0)

        # 回复列表（递归处理）
        self.reply_list = [
            Comment(reply) for reply in comment_data.get("reply_list", [])
        ]

    def __repr__(self):
        return f"Comment(id={self.comment_id}, author={self.author_name}, content={self.content[:20]}...)"

    def get_comment_details(self):
        # 获取评论的详细信息
        details = {
            "comment_id": self.comment_id,
            "author_name": self.author_name,
            "content": self.content,
            "create_time": self.create_time,
            "create_time_text": self.create_time_text,
            "like_count": self.like_count,
            "reply_count": self.reply_count,
            "is_anonymous": self.is_anonymous,
            # "reply_list": [reply.get_comment_details() for reply in self.reply_list],  # 获取每个回复的详情
        }
        return details
