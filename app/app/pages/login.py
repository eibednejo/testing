import reflex as rx
from app.states.auth_state import AuthState


def login_form() -> rx.Component:
    return rx.el.form(
        rx.el.div(
            rx.el.label(
                "Email", class_name="text-sm font-medium"
            ),
            rx.el.input(
                name="email",
                type="email",
                placeholder="user@example.com",
                class_name="w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg focus:outline-none focus:ring focus:ring-blue-200",
                required=True,
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.label(
                "Password", class_name="text-sm font-medium"
            ),
            rx.el.input(
                name="password",
                type="password",
                placeholder="••••••••",
                class_name="w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg focus:outline-none focus:ring focus:ring-blue-200",
                required=True,
            ),
            class_name="mb-6",
        ),
        rx.el.button(
            "Sign In",
            type="submit",
            class_name="w-full py-2 px-4 bg-blue-500 text-white font-semibold rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50",
        ),
        on_submit=AuthState.login,
        reset_on_submit=True,
    )


def login() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "bot",
                        size=32,
                        class_name="text-blue-500",
                    ),
                    class_name="p-3 bg-blue-100 rounded-full mb-4",
                ),
                rx.el.h1(
                    "Welcome Back",
                    class_name="text-2xl font-bold text-gray-800",
                ),
                rx.el.p(
                    "Log in to continue to the AI Chat.",
                    class_name="text-gray-500",
                ),
                class_name="text-center mb-8",
            ),
            login_form(),
            class_name="w-full max-w-md bg-white p-8 rounded-2xl shadow-sm border border-gray-100",
        ),
        class_name="flex items-center justify-center min-h-screen bg-gray-50 font-['Inter']",
    )