from typing import Optional

from sqlmodel import Field, SQLModel, create_engine


class CommentHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    video_title: str
    video_description: str
    comment: str
    sexual_content: bool
    hate_speech: bool
    private_info: bool
    graphic_content: bool
    violence: bool
    spam_or_scam: bool
    impersonation: bool


engine = create_engine("sqlite:///comment_history.db")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
