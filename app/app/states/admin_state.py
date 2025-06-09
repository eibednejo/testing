# admin_state.py
import reflex as rx
from .db import users, database
from .auth_state import AuthState
import bcrypt

class AdminState(AuthState):
    user_list: list[dict] = []

    async def load_users(self):
        query = users.select()
        all_users = await database.fetch_all(query)
        # Convert to dict list for UI
        self.user_list = [
            {"email": user["email"], "is_admin": user["is_admin"]} for user in all_users
        ]

    @rx.event
    async def add_user(self, form_data: dict[str, str]):
        if not self.is_admin:
            return rx.toast.error("Access denied.")
        email = form_data["email"].lower()
        password = form_data["password"]
        is_admin = form_data.get("is_admin", False)

        if not email or not password:
            return rx.toast.error("Email and password required.")
        user = await database.fetch_one(users.select().where(users.c.email == email))
        if user:
            return rx.toast.error("User already exists.")

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        await database.execute(
            users.insert().values(email=email, hashed_password=hashed.decode(), is_admin=is_admin)
        )
        await self.load_users()
        return rx.toast.success(f"User {email} added.")

    @rx.event
    async def delete_user(self, email: str):
        if not self.is_admin:
            return rx.toast.error("Access denied.")
        await database.execute(users.delete().where(users.c.email == email))
        await self.load_users()
        return rx.toast.success(f"User {email} deleted.")

    @rx.event
    async def update_password(self, email: str, new_password: str):
        if not self.is_admin:
            return rx.toast.error("Access denied.")
        if not new_password:
            return rx.toast.error("Password cannot be empty.")
        hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        await database.execute(
            users.update()
            .where(users.c.email == email)
            .values(hashed_password=hashed.decode())
        )
        await self.load_users()
        return rx.toast.success(f"Password updated for {email}.")