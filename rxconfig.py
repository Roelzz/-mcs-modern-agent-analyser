import os

from dotenv import load_dotenv
import reflex as rx

load_dotenv()

_env = os.getenv("REFLEX_ENV", "dev")

if _env == "prod":
    _port = int(os.getenv("PORT", "2009"))
    _port_cfg = {"frontend_port": _port, "backend_port": _port}
else:
    _port_cfg = {
        "frontend_port": int(os.getenv("FRONTEND_PORT", "3000")),
        "backend_port": int(os.getenv("BACKEND_PORT", "8000")),
    }

config = rx.Config(
    app_name="web",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.RadixThemesPlugin(
            theme=rx.theme(
                accent_color="grass",
                gray_color="sand",
                radius="large",
                appearance="inherit",
            )
        ),
    ],
    **_port_cfg,
)
