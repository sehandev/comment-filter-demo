from typing import Optional

from sqlmodel import Field, SQLModel, create_engine


class CommentHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    video_title: str
    video_url: str
    comment: str
    sexual_content: bool
    sexual_content_reason: str
    violence_or_abusive: bool
    violence_or_abusive_reason: str
    hate_or_malicious: bool
    hate_or_malicious_reason: str
    harassment_or_bullying: bool
    harassment_or_bullying_reason: str
    harmful_or_dangerous_acts: bool
    harmful_or_dangerous_acts_reason: str
    misinformation: bool
    misinformation_reason: str
    child_abuse: bool
    child_abuse_reason: str
    terrorism_promotion: bool
    terrorism_promotion_reason: str
    spam_or_confusion: bool
    spam_or_confusion_reason: str


engine = create_engine("sqlite:///comment_history.db")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
