from comment_filter_demo.category import Category
from comment_filter_demo.filter import CommentFilter

filter = CommentFilter()
print(
    filter.filter(
        video_title='"이제부터 진보·보수의 문제란 없습니다." 이재명 대통령 취임사',
        comment="많이들 죽어나가겠네 ~ 그래 다 쥑이삐라 ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ",
        category=Category.spam_or_confusion,
    )
)
