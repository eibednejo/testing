import reflex as rx
from app.states.chat_state import ChatState
from app.states.file_state import FileState
from app.states.auth_state import AuthState


def file_upload_section() -> rx.Component:
    return rx.el.div(
        rx.upload.root(
            rx.el.div(
                rx.icon("cloud_upload", class_name="size-5"),
                rx.el.p("Upload CSV Files", class_name="text-sm font-medium"),
                class_name=(
                    "flex flex-col items-center gap-2 cursor-pointer text-gray-600 "
                    "hover:text-gray-900 hover:bg-gray-200 rounded-lg"
                ),
            ),
            id="file_upload",
            multiple=True,
            on_drop=FileState.handle_upload(
                rx.upload_files(upload_id="file_upload")
            ),
            accept={"text/csv": [".csv"]},
            class_name="w-full py-3 px-4",  # padding here
        ),
        rx.el.div(
            rx.foreach(
                FileState.uploaded_files,
                lambda filename: rx.el.div(
                    rx.el.div(
                        rx.icon("file", class_name="size-4 text-gray-500"),
                        rx.el.p(
                            filename,
                            class_name="text-sm truncate",
                            max_w="200px",
                        ),
                        class_name="flex items-center gap-2 flex-grow min-w-0",
                    ),
                    rx.el.button(
                        rx.icon("trash-2", class_name="size-3"),
                        on_click=lambda: FileState.delete_file(filename),
                        class_name="p-1 text-gray-500 hover:text-red-600 rounded-md",
                    ),
                    class_name="flex items-center justify-between p-2 bg-gray-100 rounded-md",
                ),
            ),
            class_name="flex flex-col gap-2 mt-2 max-h-40 overflow-y-auto",
        ),
        # Remove border here to eliminate bottom border line below upload section
        # class_name="border-b border-gray-200",
    )


def sidebar_chat_item(chat: dict[str, str]) -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.cond(
                ChatState.editing_chat_id == chat["id"],
                rx.el.form(
                    rx.el.input(
                        name="new_title",
                        default_value=chat["title"],
                        on_blur=ChatState.rename_chat_from_input,
                        class_name="w-full text-sm font-medium bg-transparent border-none p-0 focus:outline-none",
                        on_click=rx.prevent_default,
                        auto_focus=True,
                    ),
                    on_submit=ChatState.rename_chat_from_form,
                    reset_on_submit=True,
                ),
                rx.el.p(chat["title"], class_name="truncate text-sm font-medium"),
            ),
            on_click=lambda: ChatState.select_chat(chat["id"]),
            class_name=rx.cond(
                ChatState.current_chat_id == chat["id"],
                "w-full p-3 rounded-lg text-left bg-blue-100 text-blue-600",
                "w-full p-3 rounded-lg text-left text-gray-600 hover:bg-gray-100",
            ),
            width="100%",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("pencil", size=14),
                on_click=[
                    rx.prevent_default,
                    lambda: ChatState.set_editing_chat(chat["id"]),
                ],
                class_name="p-1 text-gray-500 hover:text-gray-800 hover:bg-gray-200 rounded-md",
            ),
            rx.el.button(
                rx.icon("trash-2", size=14),
                on_click=[
                    rx.prevent_default,
                    lambda: ChatState.delete_chat(chat["id"]),
                ],
                class_name="p-1 text-gray-500 hover:text-red-600 hover:bg-red-100 rounded-md",
            ),
            class_name=rx.cond(
                (ChatState.current_chat_id == chat["id"])
                & (ChatState.editing_chat_id != chat["id"]),
                "absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity",
                "hidden",
            ),
        ),
        class_name="relative group w-full",
    )

def sidebar() -> rx.Component:
    return rx.el.div(
        # Header
        rx.el.div(
            rx.el.div(
                rx.icon("bot", class_name="size-6 text-gray-700"),
                rx.el.p(
                    "Benwara Analitik Global",
                    class_name="font-semibold text-gray-800",
                ),
                class_name="flex flex-col items-center gap-1",
            ),
            class_name="flex items-center justify-center px-4 py-3 border-b border-gray-200",
        ),

        # Conversations header + new chat
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Conversations",
                    class_name="text-lg font-semibold text-gray-700 text-center flex-grow",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("circle-plus", size=24),
                        on_click=ChatState.new_chat,
                        class_name="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-200 rounded-md",
                    ),
                    rx.el.span(
                        "New Chat",
                        class_name=(
                            "absolute z-50 hidden group-hover:block text-xs text-white "
                            "bg-gray-800 rounded px-2 py-1 bottom-full mb-2 left-1/2 "
                            "-translate-x-1/2 whitespace-nowrap shadow"
                        ),
                    ),
                    class_name="relative group",
                ),
                class_name="flex items-center justify-center gap-2 px-4 py-3",
            ),
            class_name="border-b border-gray-200",
        ),

        # Scrollable chat list (takes available vertical space)
        rx.el.div(
            rx.foreach(ChatState.sorted_chat_titles, sidebar_chat_item),
            class_name="flex-grow px-4 py-3 space-y-1 overflow-y-auto",
            style={"minHeight": "0"},
        ),

        # Scrollable uploaded files list below chat list, fixed height
        rx.el.div(
            rx.foreach(FileState.uploaded_files, lambda filename: rx.el.div(
                rx.el.div(
                    rx.icon("file", class_name="size-4 text-gray-500"),
                    rx.el.p(
                        filename,
                        class_name="text-sm truncate max-w-[100px]"
                    ),
                    class_name="flex items-center gap-2 flex-grow min-w-0",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="size-3"),
                    on_click=lambda: FileState.delete_file(filename),
                    class_name="p-1 text-gray-500 hover:text-red-600 rounded-md",
                ),
                class_name="flex items-center justify-between p-2 bg-gray-100 rounded-md",
            )),
            class_name="px-4 py-2 overflow-y-auto border-t border-gray-200",
            style={"height": "140px", "minHeight": "140px"},
        ),

        # Fixed file upload section above footer
        rx.el.div(
            file_upload_section(),
            class_name=(
                "absolute left-0 right-0 bg-gray-50 border-t border-gray-200 "
                "px-4 py-3"
            ),
            style={"height": "250px", "bottom": "64px", "zIndex": "20"},
        ),

        # Footer fixed at bottom
        rx.el.div(
            rx.el.div(
                rx.el.img(
                    src=f"https://api.dicebear.com/9.x/initials/svg?seed={AuthState.current_user}",
                    class_name="size-8 rounded-full",
                ),
                rx.el.div(
                    rx.el.p(
                        AuthState.current_user,
                        class_name="text-sm font-semibold truncate",
                    ),
                    class_name="flex-grow min-w-0",
                ),
                rx.el.button(
                    rx.icon("log-out", size=16),
                    on_click=AuthState.logout,
                    class_name="p-2 text-gray-500 hover:text-red-600 hover:bg-red-100 rounded-md",
                ),
                class_name="flex items-center gap-3 w-full",
            ),
            class_name=(
                "absolute bottom-0 left-0 right-0 bg-gray-50 border-t border-gray-200 "
                "p-4"
            ),
            style={"height": "64px", "zIndex": "30"},
        ),

        # Sidebar container with relative for absolute positioning
        class_name="relative flex flex-col h-screen w-72 bg-gray-50 border-r border-gray-200 font-['Inter']",
    )