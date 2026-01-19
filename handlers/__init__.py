from aiogram import Router
from .start import router as start_router
from .profile import router as profile_router
from .water import router as water_router
from .food import router as food_router
from .workout import router as workout_router
from .progress import router as progress_router

router = Router()
router.include_router(start_router)
router.include_router(profile_router)
router.include_router(water_router)
router.include_router(food_router)
router.include_router(workout_router)
router.include_router(progress_router)