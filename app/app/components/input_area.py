import reflex as rx
from ..states.chat_state import ChatState


def input_area() -> rx.Component:
    return rx.el.form(
        rx.el.div(
            rx.el.textarea(
                on_change=ChatState.set_current_message,
                placeholder="Type a message...",
                class_name=(
                    "w-full bg-transparent focus:outline-none resize-none "
                    "text-mauve-12 dark:text-mauve-12 placeholder-mauve-9 dark:placeholder-mauve-8 "
                    "py-3 pl-4 pr-12 text-base border-2 border-mauve-9 dark:border-mauve-8 rounded-md"
                ),
                rows=1,
                default_value=ChatState.current_message,
                enter_key_submit=True,
            ),
            rx.el.button(
                rx.cond(
                    ChatState.is_typing,
                    rx.icon(
                        "loader-circle",
                        class_name="animate-spin",
                    ),
                    rx.icon("arrow-up"),
                ),
                type="submit",
                disabled=ChatState.is_typing
                | (ChatState.current_message.strip() == ""),
                class_name=(
                    "absolute right-2 top-1/2 -translate-y-1/2 size-8 "
                    "bg-blue-500 text-white rounded-full flex items-center justify-center "
                    "hover:bg-blue-600 disabled:bg-blue-300 transition-colors"
                ),
            ),
            class_name="relative flex items-center w-full",  # ensure this div is full width
        ),
        on_submit=ChatState.send_message,
        reset_on_submit=True,
        class_name="w-full",  # ensure form is full width
    )



def chat_footer() -> rx.Component:
    return rx.el.div(
        input_area(),
        class_name="w-full max-w-8xl mx-auto px-4 sm:px-6 pb-4 pt-2 flex flex-col",
    )

def chat_header() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("bot", class_name="size-6 text-gray-700"),
            rx.el.p(
                "Hello, I'm MasNalis, your personal AI-powered Data Analyst",
                class_name="font-semibold text-gray-800 text-base",
            ),
            class_name="flex items-center gap-3",
        ),
        # Add more elements here on the right if needed
        class_name="flex items-center justify-between p-4 border-b border-gray-200",
    )