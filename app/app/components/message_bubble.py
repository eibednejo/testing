import reflex as rx
from .typing_indicator import typing_indicator


def ai_bubble(
    message: str, is_last_message: bool
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("bot", size=20),
            class_name="flex-shrink-0 size-8 bg-gray-200 text-gray-700 rounded-full flex items-center justify-center",
        ),
        rx.el.div(
            rx.cond(
                (message == "") & is_last_message,
                typing_indicator(),
                rx.markdown(
                    message,
                    class_name="text-sm sm:text-base",
                    component_map={
                        "p": lambda *children: rx.el.p(
                            *children, class_name="mb-0 last:mb-0"
                        ),
                        "h1": lambda *children: rx.el.h1(
                            *children,
                            class_name="text-xl font-bold my-4"
                        ),
                        "h2": lambda *children: rx.el.h2(
                            *children,
                            class_name="text-lg font-semibold my-3"
                        ),
                        "h3": lambda *children: rx.el.h3(
                            *children,
                            class_name="text-base font-semibold my-2"
                        ),
                        "code": lambda *children: rx.el.code(
                            *children,
                            class_name="bg-gray-200 p-1 rounded-sm text-sm"
                        ),
                        "codeblock": lambda text, **props: rx.el.div(
                            rx.code_block(
                                text, **props, theme="light"
                            ),
                            class_name="my-4",
                        ),
                    },
                ),
            ),
            class_name="bg-gray-100 text-gray-800 rounded-2xl py-3 px-3 max-w-4xl text-sm sm:text-base",
        ),
        class_name="flex items-start gap-3",
    )


def user_bubble(message: str) -> rx.Component:
    return rx.el.div(
        rx.el.p(message, class_name="text-sm sm:text-base"),
        class_name="bg-blue-500 text-white rounded-2xl p-3 max-w-3xl ml-auto",
    )


def message_bubble(
    message: dict, index: int
) -> rx.Component:
    from ..states.chat_state import ChatState

    is_last = index == ChatState.messages.length() - 1
    return rx.el.div(
        rx.cond(
            message["is_ai"],
            ai_bubble(message["text"], is_last),
            user_bubble(message["text"]),
        ),
        class_name="w-full",
    )