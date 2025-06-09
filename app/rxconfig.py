import reflex as rx

config = rx.Config(app_name="app")

def setup_routes():
    from app.pages import main, login, admin
    config.routes = {
        "/": main.MainPage,
        "/login": login.LoginPage,
        "/admin": admin.AdminPage,
    }

setup_routes()