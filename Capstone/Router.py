from fastapi import APIRouter, HTTPException, status
from services.UserService import register_new_user
from Model.UserModel import UserRegisterRequest, UserLoginRequest

user_router = APIRouter(tags=["user"])

@user_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegisterRequest):

    try:
        user_id = await register_new_user(user_data)

        return {
            "message": "계좌 등록이 성공했습니다!",
            "user_id": user_id,
            "username": user_data.username
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal Server Error")
