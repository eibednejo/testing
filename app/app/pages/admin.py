class AdminPage(rx.Component):
    def render(self):
        admin = rx.use_state(AdminState)

        add_user_form = rx.form(
            on_submit=admin.add_user,
            rx.box(
                rx.input(type="email", name="email", placeholder="Email"),
                rx.input(type="password", name="password", placeholder="Password"),
                rx.checkbox(name="is_admin"),
                rx.label("Is Admin"),
                rx.button("Add User", type="submit"),
                spacing="10px",
                padding="10px",
                border="1px solid lightgray",
                border_radius="5px",
            )
        )

        user_rows = [
            rx.box(
                key=user["email"],
                rx.text(user["email"]),
                rx.text(" (Admin)") if user["is_admin"] else rx.text(" (User)"),
                rx.input(
                    type="password",
                    placeholder="New password",
                    on_change=lambda val, email=user["email"]: admin.update_password(email, val),
                ),
                rx.button("Delete", on_click=lambda email=user["email"]: admin.delete_user(email)),
                spacing="10px",
                margin_bottom="10px",
                padding="10px",
                border="1px solid lightgray",
                border_radius="5px",
            )
            for user in admin.user_list
        ]

        return rx.box()(
            rx.heading("Admin User Management"),
            add_user_form,
            rx.div(user_rows),
            rx.button("Back to Home", on_click=lambda: rx.redirect("/")),
            padding="20px",
            max_width="600px",
            margin="auto"
        )