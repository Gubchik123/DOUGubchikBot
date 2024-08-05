from aiogram import Router

from .menu import router as menu_router


vacancy_router = Router()

vacancy_router.include_routers(menu_router)
