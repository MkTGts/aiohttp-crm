from aiohttp.web import Application as AiohttpAplication, run_app as aiohttp_run_app, View as AiohttpView, Request as AiohttpRequset
from app.crm.routes import setup_routes
from typing import Optional, TYPE_CHECKING
from app.store.crm.accessor import CrmAccessor
from app.store import setup_accessor


class Application(AiohttpAplication):
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


app = AiohttpAplication()


def run_app():
    setup_routes(app)
    setup_accessor(app)
    aiohttp_run_app(app)