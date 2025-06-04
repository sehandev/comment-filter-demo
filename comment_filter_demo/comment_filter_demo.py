"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from comment_filter_demo.ai_manager import AI_Manager
from comment_filter_demo.db import CommentHistory, create_db_and_tables, engine

load_dotenv()


class State(rx.State):
    """The app state."""

    video_title: str
    video_description: str
    comment: str
    comment_history: list[CommentHistory] = []

    ai_manager: AI_Manager = AI_Manager(model_name="gemini-2.5-flash")

    spam_results: dict[str, bool] = {
        "sexual_content": False,
        "hate_speech": False,
        "private_info": False,
        "graphic_content": False,
        "violence": False,
        "spam_or_scam": False,
        "impersonation": False,
    }
    spam_reasons: dict[str, str] = {
        "sexual_content": "",
        "hate_speech": "",
        "private_info": "",
        "graphic_content": "",
        "violence": "",
        "spam_or_scam": "",
        "impersonation": "",
    }

    def run_spam_filter(self):
        # Use the AI_Manager to get results
        # For now, keep the mock logic for demonstration
        self.ai_manager.model_name = "gemini-2.5-flash"  # Example, can be dynamic
        response = self.ai_manager.get_ai_response(self.comment)

        if "sex" in self.comment.lower() or "sexual" in response.lower():
            self.spam_results["sexual_content"] = True
            self.spam_reasons["sexual_content"] = (
                "Comment contains sexual keywords."
                if "sex" in self.comment.lower()
                else "AI detected sexual content."
            )
        else:
            self.spam_results["sexual_content"] = False
            self.spam_reasons["sexual_content"] = ""

        if "hate" in self.comment.lower() or "hate speech" in response.lower():
            self.spam_results["hate_speech"] = True
            self.spam_reasons["hate_speech"] = (
                "Comment contains hate speech keywords."
                if "hate" in self.comment.lower()
                else "AI detected hate speech."
            )
        else:
            self.spam_results["hate_speech"] = False
            self.spam_reasons["hate_speech"] = ""

        if (
            "private" in self.comment.lower()
            or "private information" in response.lower()
        ):
            self.spam_results["private_info"] = True
            self.spam_reasons["private_info"] = (
                "Comment contains private information."
                if "private" in self.comment.lower()
                else "AI detected private information."
            )
        else:
            self.spam_results["private_info"] = False
            self.spam_reasons["private_info"] = ""

        if "graphic" in self.comment.lower() or "graphic content" in response.lower():
            self.spam_results["graphic_content"] = True
            self.spam_reasons["graphic_content"] = (
                "Comment contains graphic content."
                if "graphic" in self.comment.lower()
                else "AI detected graphic content."
            )
        else:
            self.spam_results["graphic_content"] = False
            self.spam_reasons["graphic_content"] = ""

        if "violence" in self.comment.lower() or "violence" in response.lower():
            self.spam_results["violence"] = True
            self.spam_reasons["violence"] = (
                "Comment contains violence related keywords."
                if "violence" in self.comment.lower()
                else "AI detected violence."
            )
        else:
            self.spam_results["violence"] = False
            self.spam_reasons["violence"] = ""

        if (
            "spam" in self.comment.lower()
            or "scam" in self.comment.lower()
            or "spam" in response.lower()
            or "scam" in response.lower()
        ):
            self.spam_results["spam_or_scam"] = True
            self.spam_reasons["spam_or_scam"] = (
                "Comment contains spam keywords."
                if "spam" in self.comment.lower() or "scam" in self.comment.lower()
                else "AI detected spam or scam."
            )
        else:
            self.spam_results["spam_or_scam"] = False
            self.spam_reasons["spam_or_scam"] = ""

        if "impersonate" in self.comment.lower() or "impersonation" in response.lower():
            self.spam_results["impersonation"] = True
            self.spam_reasons["impersonation"] = (
                "Comment contains impersonation keywords."
                if "impersonate" in self.comment.lower()
                else "AI detected impersonation."
            )
        else:
            self.spam_results["impersonation"] = False
            self.spam_reasons["impersonation"] = ""

        with Session(engine) as session:
            history_entry = CommentHistory(
                video_title=self.video_title,
                video_description=self.video_description,
                comment=self.comment,
                sexual_content=self.spam_results["sexual_content"],
                hate_speech=self.spam_results["hate_speech"],
                private_info=self.spam_results["private_info"],
                graphic_content=self.spam_results["graphic_content"],
                violence=self.spam_results["violence"],
                spam_or_scam=self.spam_results["spam_or_scam"],
                impersonation=self.spam_results["impersonation"],
            )
            session.add(history_entry)
            session.commit()

    def load_comment_history(self):
        with Session(engine) as session:
            self.comment_history = session.query(CommentHistory).all()


@rx.page(route="/")
def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Comment Filter App", size="9"),
            rx.link(rx.button("Go to Test Page"), href="/test"),
            rx.link(rx.button("Go to History Page"), href="/history"),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
        rx.logo(),
    )


@rx.page(route="/test")
def test_page() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Test Page", size="9"),
            rx.input(
                placeholder="Video Title",
                on_change=State.set_video_title,
                width="100%",
            ),
            rx.text_area(
                placeholder="Video Description",
                on_change=State.set_video_description,
                width="100%",
            ),
            rx.text_area(
                placeholder="Comment",
                on_change=State.set_comment,
                width="100%",
            ),
            rx.button("Run Filter", on_click=State.run_spam_filter),
            rx.foreach(
                State.spam_results.keys(),
                lambda category: rx.hstack(
                    rx.text(category),
                    rx.cond(
                        State.spam_results[category],
                        rx.text("True", color="red"),
                        rx.text("False", color="green"),
                    ),
                    rx.text(State.spam_reasons[category]),
                ),
            ),
            rx.button("Back to Home", on_click=rx.redirect("/")),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )


@rx.page(route="/history", on_load=State.load_comment_history)
def history_page() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("History Page", size="9"),
            rx.foreach(
                State.comment_history,
                lambda entry: rx.vstack(
                    rx.text(f"Video Title: {entry.video_title}"),
                    rx.text(f"Video Description: {entry.video_description}"),
                    rx.text(f"Comment: {entry.comment}"),
                    rx.divider(),
                ),
            ),
            rx.button("Back to Home", on_click=rx.redirect("/")),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )


app = rx.App()

create_db_and_tables()
