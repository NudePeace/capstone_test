# File: routers/user.py (Cần tạo file này)

from fastapi import APIRouter, HTTPException, status
from services.userServices.user import register_new_user

# Đảm bảo đã sửa import này trong services/user.py
from models.user import UserRegisterRequest

user_router = APIRouter(tags=["Users"])


@user_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegisterRequest):
    """
    Endpoint xử lý việc đăng ký tài khoản mới.
    """

    try:
        user_id = await register_new_user(user_data)

        return {
            "message": "Đăng ký tài khoản thành công!",
            "user_id": user_id,
            "username": user_data.username
        }
    except ValueError as e:
        # Lỗi trùng lặp từ database.py
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        # Các lỗi hệ thống hoặc DB khác
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Lỗi hệ thống không xác định khi đăng ký.")