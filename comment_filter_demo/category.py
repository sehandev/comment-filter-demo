class Category:
    sexual_content: str = "sexual_content"
    hate_speech: str = "hate_speech"
    private_info: str = "private_info"
    graphic_content: str = "graphic_content"
    violence: str = "violence"
    spam_or_scam: str = "spam_or_scam"
    impersonation: str = "impersonation"

    def __init__(self):
        pass

    def get_prompt(self, category: str) -> str:
        match category:
            case Category.sexual_content:
                return self.get_sexual_content_prompt()
            case Category.hate_speech:
                return self.get_hate_speech_prompt()
            case Category.private_info:
                return self.get_private_info_prompt()
            case Category.graphic_content:
                return self.get_graphic_content_prompt()
            case Category.violence:
                return self.get_violence_prompt()
            case Category.spam_or_scam:
                return self.get_spam_or_scam_prompt()
            case Category.impersonation:
                return self.get_impersonation_prompt()
            case _:
                raise ValueError(f"Invalid category: {category}")

    def get_sexual_content_prompt(self) -> str:
        return "Is the comment sexual content?"
