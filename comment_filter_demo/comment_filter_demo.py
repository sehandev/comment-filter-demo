from typing import Optional

import reflex as rx
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from comment_filter_demo.category import Category
from comment_filter_demo.db import CommentHistory, create_db_and_tables, engine
from comment_filter_demo.filter import CommentFilter

load_dotenv()


class State(rx.State):
    """The app state."""

    video_title: str
    video_description: str
    comment: str
    comment_history: list[CommentHistory] = []

    spam_results: dict[str, Optional[bool]] = {
        "sexual_content": None,
        "violence_or_abusive": None,
        "hate_or_malicious": None,
        "harassment_or_bullying": None,
        "harmful_or_dangerous_acts": None,
        "misinformation": None,
        "child_abuse": None,
        "terrorism_promotion": None,
        "spam_or_confusion": None,
    }
    spam_reasons: dict[str, str] = {
        "sexual_content": "",
        "violence_or_abusive": "",
        "hate_or_malicious": "",
        "harassment_or_bullying": "",
        "harmful_or_dangerous_acts": "",
        "misinformation": "",
        "child_abuse": "",
        "terrorism_promotion": "",
        "spam_or_confusion": "",
    }

    def run_spam_filter(self):
        comment_filter_instance = CommentFilter()
        category_instance = Category()

        for category_name in category_instance.get_all_prompts():
            is_spam = comment_filter_instance.filter(
                self.video_title,
                self.video_description,
                self.comment,
                category_name,
            )
            # Currently, the filter method only returns a boolean, not a reason.
            # You might want to extend CommentFilter to return a reason as well.
            reason = (
                "AI filtered based on category criteria."
                if is_spam
                else "Not detected."
            )

            self.spam_results[category_name] = is_spam
            self.spam_reasons[category_name] = reason

        with Session(engine) as session:
            history_entry = CommentHistory(
                video_title=self.video_title,
                video_description=self.video_description,
                comment=self.comment,
                sexual_content=self.spam_results["sexual_content"],
                violence_or_abusive=self.spam_results["violence_or_abusive"],
                hate_or_malicious=self.spam_results["hate_or_malicious"],
                harassment_or_bullying=self.spam_results["harassment_or_bullying"],
                harmful_or_dangerous_acts=self.spam_results[
                    "harmful_or_dangerous_acts"
                ],
                misinformation=self.spam_results["misinformation"],
                child_abuse=self.spam_results["child_abuse"],
                terrorism_promotion=self.spam_results["terrorism_promotion"],
                spam_or_confusion=self.spam_results["spam_or_confusion"],
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
