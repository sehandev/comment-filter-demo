class Category:
    sexual_content: str = "sexual_content"
    violence_or_abusive: str = "violence_or_abusive"
    hate_or_malicious: str = "hate_or_malicious"
    harassment_or_bullying: str = "harassment_or_bullying"
    harmful_or_dangerous_acts: str = "harmful_or_dangerous_acts"
    misinformation: str = "misinformation"
    child_abuse: str = "child_abuse"
    terrorism_promotion: str = "terrorism_promotion"
    spam_or_confusion: str = "spam_or_confusion"

    def __init__(self):
        pass

    def get_prompt(self, category: str, comment: str, video_title: str) -> str:
        match category:
            case Category.sexual_content:
                return self.get_sexual_content_prompt(comment, video_title)
            case Category.violence_or_abusive:
                return self.get_violence_or_abusive_prompt(comment, video_title)
            case Category.hate_or_malicious:
                return self.get_hate_or_malicious_prompt(comment, video_title)
            case Category.harassment_or_bullying:
                return self.get_harassment_or_bullying_prompt(comment, video_title)
            case Category.harmful_or_dangerous_acts:
                return self.get_harmful_or_dangerous_acts_prompt(comment, video_title)
            case Category.misinformation:
                return self.get_misinformation_prompt(comment, video_title)
            case Category.child_abuse:
                return self.get_child_abuse_prompt(comment, video_title)
            case Category.terrorism_promotion:
                return self.get_terrorism_promotion_prompt(comment, video_title)
            case Category.spam_or_confusion:
                return self.get_spam_or_confusion_prompt(comment, video_title)
            case _:
                raise ValueError(f"Invalid category: {category}")

    def get_sexual_content_prompt(self, comment: str, video_title: str) -> str:
        return f"Given the video title: '{video_title}', is the following comment sexual content? Reply with 'True' or 'False'. Comment: {comment}"

    def get_violence_or_abusive_prompt(self, comment: str, video_title: str) -> str:
        return f"Given the video title: '{video_title}', is the following comment violent or abusive content? Reply with 'True' or 'False'. Comment: {comment}"

    def get_hate_or_malicious_prompt(self, comment: str, video_title: str) -> str:
        return f"Given the video title: '{video_title}', is the following comment hate speech or malicious content? Reply with 'True' or 'False'. Comment: {comment}"

    def get_harassment_or_bullying_prompt(self, comment: str, video_title: str) -> str:
        return f"Given the video title: '{video_title}', is the following comment harassment or bullying content? Reply with 'True' or 'False'. Comment: {comment}"

    def get_harmful_or_dangerous_acts_prompt(
        self, comment: str, video_title: str
    ) -> str:
        return f"Given the video title: '{video_title}', is the following comment harmful or dangerous acts content? Reply with 'True' or 'False'. Comment: {comment}"

    def get_misinformation_prompt(self, comment: str, video_title: str) -> str:
        return f"Given the video title: '{video_title}', is the following comment misinformation? Reply with 'True' or 'False'. Comment: {comment}"

    def get_child_abuse_prompt(self, comment: str, video_title: str) -> str:
        return f"Given the video title: '{video_title}', is the following comment child abuse content? Reply with 'True' or 'False'. Comment: {comment}"

    def get_terrorism_promotion_prompt(self, comment: str, video_title: str) -> str:
        return f"Given the video title: '{video_title}', is the following comment terrorism promotion content? Reply with 'True' or 'False'. Comment: {comment}"

    def get_spam_or_confusion_prompt(self, video_title: str, comment: str) -> str:
        return f"""
        Is the following comment spam or confusing content?

        Video Title: 백종원은 회생할 수 있을까? 백종원과 미디어가 서로를 이용하는 법!
        Comment: I am an ugly bag of mostly water.
        Result: True
        Reason: The comment "I am an ugly bag of mostly water" is completely irrelevant to the video's title, "Can Baek Jong-won recover? How Baek Jong-won and the media use each other!" It appears to be a random, nonsensical statement with no connection to the discussion, making it confusing and potentially spam-like.
        
        Video Title: {video_title}
        Comment: {comment}
        Result: 
        """

    def get_all_prompts(self) -> dict:
        return {
            Category.sexual_content,
            Category.violence_or_abusive,
            Category.hate_or_malicious,
            Category.harassment_or_bullying,
            Category.harmful_or_dangerous_acts,
            Category.misinformation,
            Category.child_abuse,
            Category.terrorism_promotion,
            Category.spam_or_confusion,
        }
