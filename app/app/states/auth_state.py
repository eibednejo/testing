# auth_state.py
import reflex as rx
import bcrypt
from typing import Optional

class AuthState(rx.State):
    session_email: Optional[str] = None
    session_is_admin: bool = False

    @rx.var
    def is_authenticated(self) -> bool:
        return self.session_email is not None

    @rx.var
    def is_admin(self) -> bool:
        return self.session_is_admin
    
    @rx.var
    def current_user(self) -> str:
        """Return the current user's email or a default value"""
        return self.session_email or "Guest"
    
    def protected_route(self):
        """Redirect to login if user is not authenticated"""
        if not self.is_authenticated:
            return rx.redirect("/login")
    
    @rx.event
    async def logout(self):
        """Log out the current user"""
        self.session_email = None
        self.session_is_admin = False
        return rx.redirect("/login")

    async def hash_password(self, password: str) -> bytes:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    async def verify_password(self, password: str, hashed: bytes) -> bool:
        return bcrypt.checkpw(password.encode(), hashed)

    @rx.event
    async def login(self, form_data: dict[str, str]):
        # Import only when needed
        from app.states.db import database, users
        
        email = form_data.get("email", "").lower()
        password = form_data.get("password", "")
        query = users.select().where(users.c.email == email)
        user = await database.fetch_one(query)
        # ... rest of your code

    @rx.event
    async def signup(self, form_data: dict[str, str]):
        # Import only when needed
        from app.states.db import database, users
        
        email = form_data.get("email", "").lower()
        password = form_data.get("password", "")
        if not email or not password:
            return rx.toast.error("Email and password cannot be empty.")

        query = users.select().where(users.c.email == email)
        user = await database.fetch_one(query)
        if user:
            return rx.toast.error("Email already exists.")

        hashed = await self.hash_password(password)
        query = users.insert().values(email=email, hashed_password=hashed.decode(), is_admin=False)
        await database.execute(query)

        self.session_email = email
        self.session_is_admin = False
        return rx.redirect("/")
    
    async def ensure_db_connected(self):
        from .db import connect_db
        await connect_db()