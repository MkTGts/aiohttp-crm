from aiohttp.web import Application as AiohttpAplication, run_app as aiohttp_run_app, View as AiohttpView, Request as AiohttpRequset
from app.crm.routes import setup_routes
from typing import Optional
from app.store.crm.accessor import CrmAccessor



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
    aiohttp_run_app(app)