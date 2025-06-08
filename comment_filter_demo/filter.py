from comment_filter_demo.ai_manager import AI_Manager
from comment_filter_demo.category import Category


class CommentFilter:
    def __init__(self, model_name: str = "gemini-2.5-pro"):
        self.model_name = model_name

    def filter(
        self,
        video_title: str,
        comment: str,
        category: str,
    ) -> tuple[bool, str]:
        ai_manager = AI_Manager(model_name=self.model_name)
        category_instance = Category()

        retries = 0
        max_retries = 3
        reason = ""
        is_spam = False

        while retries < max_retries:
            prompt = category_instance.get_prompt(category, comment, video_title)
            response = ai_manager.get_ai_response(prompt)

            is_spam = "true" in response.lower() or "yes" in response.lower()
            if "Reason: " in response:
                reason = response.split("Reason: ")[1].strip()
            else:
                reason = response.strip()

            if not is_spam or len(reason.split()) >= 3:
                break
            retries += 1

        return is_spam, reason


if __name__ == "__main__":
    filter = CommentFilter()
    print(
        filter.filter(
            video_title='"이제부터 진보·보수의 문제란 없습니다." 이재명 대통령 취임사',
            comment="많이들 죽어나가겠네 ~ 그래 다 쥑이삐라 ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ",
            category=Category.spam_or_confusion,
        )
    )
