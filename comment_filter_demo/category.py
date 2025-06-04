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
        return f"""Given the video title: '{video_title}', is the following comment sexual content? Reply with 'True' or 'False'. Comment: {comment}'

        Video Title: '남사친을 짝사랑할 수 없는 이유'
        Comment: '여자 쪽이 그냥 개섹시한데 그걸 못 잡은 남자가 병신이지.'
        Result: True
        Reason: The comment implies sexual desire and intensity.

        Video Title: {video_title}
        Comment: {comment}
        Result:
        """

    def get_violence_or_abusive_prompt(self, comment: str, video_title: str) -> str:
        return f"""Given the video title: '{video_title}', is the following comment violent or abusive content? Reply with 'True' or 'False'. Comment: {comment}'

        Video Title: '너네 반 있는지 확인 ㄱㄱ 학교마다 꼭 있는 반 유형 TOP7'
        Comment: '저 새끼 진짜 개패고 싶다. 학교 오지말라 해'
        Result: True
        Reason: The comment expresses a desire to inflict physical harm and excludes someone from school, which is abusive.

        Video Title: {video_title}
        Comment: {comment}
        Result:
        """

    def get_hate_or_malicious_prompt(self, comment: str, video_title: str) -> str:
        return f"""Given the video title: '{video_title}', is the following comment hate speech or malicious content? Reply with 'True' or 'False'. Comment: {comment}'

        Video Title: '에티오피아의 커피 문화'
        Comment: '그 나라는 사람들이 미개해서 발전이 없어.'
        Result: True
        Reason: The comment generalizes and demeans an entire nationality, which is hate speech.

        Video Title: {video_title}
        Comment: {comment}
        Result:
        """

    def get_harassment_or_bullying_prompt(self, comment: str, video_title: str) -> str:
        return f"""Given the video title: '{video_title}', is the following comment harassment or bullying content? Reply with 'True' or 'False'. Comment: {comment}'

        Video Title: '사이버 왕따의 심각성'
        Comment: '야 너 또 글 올렸냐? 작작해라 진짜 역겹네'
        Result: True
        Reason: The comment is a direct attack and uses derogatory language, indicative of online harassment.

        Video Title: {video_title}
        Comment: {comment}
        Result:
        """

    def get_harmful_or_dangerous_acts_prompt(
        self, comment: str, video_title: str
    ) -> str:
        return f"""Given the video title: '{video_title}', is the following comment harmful or dangerous acts content? Reply with 'True' or 'False'. Comment: {comment}'

        Video Title: '고층 건물에서 뛰어내리는 방법'
        Comment: '나도 저렇게 하면 죽을 수 있을까? 따라하고 싶다'
        Result: True
        Reason: The comment expresses an intent to imitate a dangerous act (jumping from a tall building) which could lead to self-harm.

        Video Title: {video_title}
        Comment: {comment}
        Result:
        """

    def get_misinformation_prompt(self, comment: str, video_title: str) -> str:
        return f"""Given the video title: '{video_title}', is the following comment misinformation? Reply with 'True' or 'False'. Comment: {comment}'

        Video Title: '코로나 바이러스 예방 수칙'
        Comment: '코로나는 사실 감기라서 마스크 쓸 필요없음. 그냥 다녀도 돼'
        Result: True
        Reason: The comment falsely claims that COVID-19 is just a cold and masks are unnecessary, which is dangerous misinformation.

        Video Title: {video_title}
        Comment: {comment}
        Result:
        """

    def get_child_abuse_prompt(self, comment: str, video_title: str) -> str:
        return f"""Given the video title: '{video_title}', is the following comment child abuse content? Reply with 'True' or 'False'. Comment: {comment}'

        Video Title: '아동 안전 교육'
        Comment: '어린애들 옷 벗겨놓고 혼내야 말 들음. 말을 안들으면 때려야지'
        Result: True
        Reason: The comment suggests physically abusing children and removing their clothes as a form of punishment, which is child abuse.

        Video Title: {video_title}
        Comment: {comment}
        Result:
        """

    def get_terrorism_promotion_prompt(self, comment: str, video_title: str) -> str:
        return f"""Given the video title: '{video_title}', is the following comment terrorism promotion content? Reply with 'True' or 'False'. Comment: {comment}'

        Video Title: '세계 평화를 위한 다큐멘터리'
        Comment: '폭탄 만들어서 정부 건물을 날려버리자. 그래야 세상이 바뀐다'
        Result: True
        Reason: The comment advocates for violent acts against government property to achieve political change, which promotes terrorism.

        Video Title: {video_title}
        Comment: {comment}
        Result:
        """

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
