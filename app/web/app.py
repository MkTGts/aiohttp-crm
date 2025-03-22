from aiohttp.web import Application as AiohttpAplication, run_app as aiohttp_run_app, View as AiohttpView, Request as AiohttpRequset
from app.crm.routes import setup_routes
from typing import Optional
from aiohttp_apispec import setup_aiohttp_apispec
from app.store.crm.accessor import CrmAccessor
from app.store import setup_accessor
from app.web.middlewares import setup_middlewares
from app.web.config import Config, setup_config


class Application(AiohttpAplication):
    config: Optional[Config] = None
    database: dict = {}
    crm_accessor: Optional[CrmAccessor] = None


class Request(AiohttpRequset):
    @property
    def app(self) -> "Application":
        return super().app()
    

class View(AiohttpView):
    @property
    def request(self) -> Request:
        return super().request


app = Application()


def run_app():
    setup_config(app)
    setup_routes(app)
    setup_aiohttp_apispec(app, tytle="CRM Application", url="/docs/json", swagger_path="/docs")
    setup_middlewares(app)
    setup_accessor(app)
    aiohttp_run_app(app)