from typing import List

import reflex as rx
from dotenv import load_dotenv
from pydantic import BaseModel
from sqlalchemy.orm import Session

from comment_filter_demo.ai_manager import AI_Manager
from comment_filter_demo.category import Category
from comment_filter_demo.db import CommentHistory, create_db_and_tables, engine
from comment_filter_demo.filter import CommentFilter

load_dotenv()


class CategoryInfo(BaseModel):
    name: str
    reason: str


class FormattedCommentHistoryEntry(BaseModel):
    video_title: str
    comment: str
    video_url: str
    categories: List[CategoryInfo]
    id: int


class State(rx.State):
    """The app state."""

    video_title: str
    video_url: str
    comment: str
    comment_history: list[CommentHistory] = []

    selected_model: str = "gemini-2.5-pro"
    available_models: list[str] = list(AI_Manager.available_model_dict.keys())

    spam_results: dict[str, bool] = {
        "sexual_content": False,
        "violence_or_abusive": False,
        "hate_or_malicious": False,
        "harassment_or_bullying": False,
        "harmful_or_dangerous_acts": False,
        "misinformation": False,
        "child_abuse": False,
        "terrorism_promotion": False,
        "spam_or_confusion": False,
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

    category_enabled: dict[str, bool] = {
        "sexual_content": False,
        "violence_or_abusive": False,
        "hate_or_malicious": False,
        "harassment_or_bullying": False,
        "harmful_or_dangerous_acts": False,
        "misinformation": False,
        "child_abuse": False,
        "terrorism_promotion": False,
        "spam_or_confusion": False,
    }

    def toggle_category(self, category_name: str):
        self.category_enabled[category_name] = not self.category_enabled[category_name]

    @rx.var
    def enabled_categories(self) -> list[str]:
        return [
            category for category, enabled in self.category_enabled.items() if enabled
        ]

    def set_selected_model(self, model_name: str):
        self.selected_model = model_name

    def run_spam_filter(self):
        comment_filter_instance = CommentFilter(model_name=self.selected_model)
        category_instance = Category()

        for category_name in category_instance.get_all_prompts():
            if not self.category_enabled[category_name]:
                self.spam_results[category_name] = False
                self.spam_reasons[category_name] = "Disabled by user."
                continue

            is_spam, reason = comment_filter_instance.filter(
                self.video_title,
                self.comment,
                category_name,
            )

            self.spam_results[category_name] = is_spam
            self.spam_reasons[category_name] = reason

        with Session(engine) as session:
            history_entry = CommentHistory(
                video_title=self.video_title,
                video_url=self.video_url,
                comment=self.comment,
                sexual_content=self.spam_results["sexual_content"],
                sexual_content_reason=self.spam_reasons["sexual_content"],
                violence_or_abusive=self.spam_results["violence_or_abusive"],
                violence_or_abusive_reason=self.spam_reasons["violence_or_abusive"],
                hate_or_malicious=self.spam_results["hate_or_malicious"],
                hate_or_malicious_reason=self.spam_reasons["hate_or_malicious"],
                harassment_or_bullying=self.spam_results["harassment_or_bullying"],
                harassment_or_bullying_reason=self.spam_reasons[
                    "harassment_or_bullying"
                ],
                harmful_or_dangerous_acts=self.spam_results[
                    "harmful_or_dangerous_acts"
                ],
                harmful_or_dangerous_acts_reason=self.spam_reasons[
                    "harmful_or_dangerous_acts"
                ],
                misinformation=self.spam_results["misinformation"],
                misinformation_reason=self.spam_reasons["misinformation"],
                child_abuse=self.spam_results["child_abuse"],
                child_abuse_reason=self.spam_reasons["child_abuse"],
                terrorism_promotion=self.spam_results["terrorism_promotion"],
                terrorism_promotion_reason=self.spam_reasons["terrorism_promotion"],
                spam_or_confusion=self.spam_results["spam_or_confusion"],
                spam_or_confusion_reason=self.spam_reasons["spam_or_confusion"],
            )
            session.add(history_entry)
            session.commit()

    def delete_comment_history(self, entry_id: int):
        with Session(engine) as session:
            entry_to_delete = (
                session.query(CommentHistory)
                .filter(CommentHistory.id == entry_id)
                .first()
            )
            if entry_to_delete:
                session.delete(entry_to_delete)
                session.commit()
                self.load_comment_history()  # Reload the history after deletion

    def load_comment_history(self):
        with Session(engine) as session:
            self.comment_history = session.query(CommentHistory).all()

    @rx.var
    def formatted_comment_history(self) -> List[FormattedCommentHistoryEntry]:
        formatted_history = []
        for entry in self.comment_history:
            entry_data = FormattedCommentHistoryEntry(
                video_title=entry.video_title,
                comment=entry.comment,
                video_url=entry.video_url,
                categories=[],
                id=entry.id,
            )
            for category_name in self.category_enabled.keys():
                is_spam = getattr(entry, category_name)
                reason = getattr(entry, f"{category_name}_reason")
                if is_spam:
                    entry_data.categories.append(
                        CategoryInfo(name=category_name, reason=reason)
                    )
            formatted_history.append(entry_data)
        return formatted_history


@rx.page(route="/")
def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Video Comment Moderation System", size="8"),
            rx.link(rx.button("Go to VCMS Page"), href="/vcms"),
            rx.link(rx.button("Go to History Page"), href="/history"),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )


@rx.page(route="/vcms")
def test_page() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("VCMS Page", size="9"),
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
            rx.input(
                placeholder="YouTube URL",
                on_change=State.set_video_url,
                width="100%",
            ),
            rx.vstack(
                rx.text("Select Model:"),
                rx.select(
                    State.available_models,
                    on_change=State.set_selected_model,
                    value=State.selected_model,
                ),
                spacing="2",
                align_items="flex-start",
            ),
            rx.vstack(
                rx.text("Toggle Categories:"),
                rx.foreach(
                    State.category_enabled.keys(),
                    lambda category: rx.hstack(
                        rx.text(category),
                        rx.switch(
                            is_checked=State.category_enabled[category],
                            on_change=lambda checked_value,
                            cat_name=category: State.toggle_category(cat_name),
                        ),
                    ),
                ),
                spacing="2",
                align_items="flex-start",
            ),
            rx.button("Run Filter", on_click=State.run_spam_filter),
            rx.foreach(
                State.enabled_categories,
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
                State.formatted_comment_history,
                lambda entry_data: rx.vstack(
                    rx.text(f"Video Title: {entry_data.video_title}"),
                    rx.video(
                        url=entry_data.video_url,
                        width="400px",
                        height="auto",
                    ),
                    rx.text(f"Comment: {entry_data.comment}"),
                    rx.foreach(
                        entry_data.categories,
                        lambda category_info: rx.hstack(
                            rx.text(f"{category_info.name.replace('_', ' ')}:"),
                            rx.text(category_info.reason),
                        ),
                    ),
                    rx.button(
                        "Remove",
                        on_click=lambda entry_id=entry_data.id: State.delete_comment_history(
                            entry_id
                        ),
                    ),
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
