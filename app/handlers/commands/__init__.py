from .cancel import router as cancel_router
from .make_teacher import router as make_teacher_router
from .menu import router as menu_router
from .start import router as start_router
from .test_producer import router as test_producer_router

command_routers = [
    cancel_router,
    make_teacher_router,
    menu_router,
    start_router,
    test_producer_router,
]
