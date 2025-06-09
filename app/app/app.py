import reflex as rx
from app.components.sidebar import sidebar
from app.components.chat_interface import chat_interface
from app.pages.login import login
from app.states.auth_state import AuthState


def index() -> rx.Component:
    return rx.el.div(
        rx.cond(
            AuthState.is_authenticated,
            rx.el.div(
                sidebar(),
                chat_interface(),
                class_name="flex w-full h-screen font-['Inter']",
            ),
            login(),
        )
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(
            rel="preconnect",
            href="https://fonts.googleapis.com",
        ),
        rx.el.link(
            rel="preconnect",
            href="https://fonts.gstatic.com",
            crossorigin="",
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, on_load=AuthState.protected_route)
app.add_page(login, route="/login")