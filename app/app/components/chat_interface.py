import reflex as rx
from app.states.chat_state import ChatState
from app.components.message_bubble import message_bubble
from app.components.preset_cards import preset_cards
from app.components.input_area import chat_footer, chat_header

def chat_interface() -> rx.Component:
    return rx.el.div(
        # Header (inside max width container)
        rx.el.div(
            chat_header(),
            class_name="max-w-6xl mx-auto w-full px-4",  # add horizontal padding inside content
        ),

        # Scrollable container - full viewport width, scrollbar at edge
        rx.el.div(
            rx.cond(
                ChatState.messages.length() > 0,
                rx.el.div(
                    rx.foreach(ChatState.messages, message_bubble),
                    class_name="flex flex-col gap-4 max-w-6xl mx-auto w-full px-4 pt-8",
                ),
                rx.el.div(
                    preset_cards(),
                    class_name="flex-grow flex items-center justify-center max-w-6xl mx-auto w-full px-4",
                ),
            ),
            class_name="flex-grow overflow-y-auto w-full",
            style={"padding": "0"},
        ),

        # Footer (inside max width container)
        rx.el.div(
            chat_footer(),
            class_name="max-w-6xl mx-auto w-full px-4",
        ),

        # Outer container - full width & height
        class_name="flex flex-col h-screen w-full bg-white",
    )