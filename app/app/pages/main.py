import reflex as rx
from app.states.auth_state import AuthState

class MainPage(rx.Component):
    def render(self):
        auth = rx.use_state(AuthState)
        return rx.box()(
            rx.heading("Welcome to the Main Page!"),
            rx.text(f"Logged in as: {auth.session_email or 'Guest'}"),
            rx.cond(
                auth.is_admin,
                rx.button("Go to Admin Panel", on_click=lambda: rx.redirect("/admin"))
            ),
            rx.button("Logout", on_click=auth.logout) if auth.is_authenticated else rx.link("Login", href="/login"),
        )