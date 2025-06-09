import reflex as rx


def typing_indicator() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="h-2 w-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.3s]"
        ),
        rx.el.div(
            class_name="h-2 w-2 bg-gray-500 rounded-full animate-bounce [animation-delay:-0.15s]"
        ),
        rx.el.div(
            class_name="h-2 w-2 bg-gray-600 rounded-full animate-bounce"
        ),
        class_name="flex gap-1.5 p-3",
    )