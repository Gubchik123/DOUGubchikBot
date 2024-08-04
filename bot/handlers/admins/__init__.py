from aiogram import Router

from .users import router as users_router
from .scheduler import router as scheduler_router


admins_router = Router()

admins_router.include_routers(users_router, scheduler_router)
