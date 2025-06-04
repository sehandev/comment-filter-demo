class CommentFilter:
    def __init__(self):
        pass

    def filter(
        self,
        video_title: str,
        video_description: str,
        comment: str,
        category: str,
    ) -> bool:
        return True


if __name__ == "__main__":
    filter = CommentFilter()
    print(filter.filter("This is a comment"))
