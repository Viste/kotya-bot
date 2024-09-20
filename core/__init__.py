from aiogram import Router


def setup_routers() -> Router:
    from . import routes

    router = Router()

    router.include_router(routes.router)

    return router
