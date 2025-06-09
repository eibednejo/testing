import reflex as rx
from app.states.chat_state import ChatState


def preset_card(
    icon: str, title: str, description: str
) -> rx.Component:
    return rx.el.button(
        rx.el.div(
            rx.icon(
                tag=icon,
                class_name="text-blue-500",
                size=20,
            ),
            rx.el.p(
                title,
                class_name="font-semibold text-gray-800",
            ),
            class_name="flex items-center gap-3",
        ),
        rx.el.p(
            description,
            class_name="text-gray-500 text-sm text-left",
        ),
        on_click=[
            lambda: ChatState.set_current_message(
                description
            ),
            ChatState.send_message,
        ],
        class_name="flex flex-col items-start gap-2 p-4 bg-white border border-gray-200 rounded-xl hover:bg-gray-50 transition-colors text-left w-full",
        type="button",
    )


def preset_cards() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "bot", size=32, class_name="text-gray-700"
            ),
            class_name="p-3 bg-gray-200 rounded-full mb-4",
        ),
        rx.el.h2(
            "How can I help you today?",
            class_name="text-2xl font-bold text-gray-800 mb-6",
        ),
        rx.el.div(
            preset_card(
                "lightbulb",
                "Get the insights",
                "What is the correlation between cancelled bookings vs new/repeat guests?",
            ),
            preset_card(
                "code",
                "Know your data",
                "List columns in hotel booking data with its respective definition",
            ),
            preset_card(
                "hotel",
                "See your growth",
                "Give me yearly bookings trends",
            ),
            preset_card(
                "file-text",
                "Find out why",
                "Conduct a diagnostic analysis about the year with highest booking",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
        ),
        class_name="flex flex-col items-center justify-center text-center p-6 w-full max-w-2xl mx-auto",
    )