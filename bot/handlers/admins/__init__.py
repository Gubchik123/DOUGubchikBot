from aiogram import Router

from .users import router as users_router


admins_router = Router()

admins_router.include_routers(users_router)
