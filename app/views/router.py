from dataclasses import dataclass
from typing import Callable

from sqlalchemy.orm import Session

RouteHandler = Callable[["AppContext"], str | None]


@dataclass
class AppContext:
    session: Session
    patient_id: int | None = None
    medicine_id: int | None = None


class Router:
    def __init__(self, routes: dict[str, RouteHandler]):
        self.routes = routes

    def run(self, start_route: str, ctx: AppContext) -> None:
        route = start_route
        while route:
            handler = self.routes[route]
            route = handler(ctx)
