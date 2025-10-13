from fastapi import FastAPI
from routers.user import user_router
from database import init_postgres_pool, close_postgres_pool


app = FastAPI(
    title="Capstone API",
    version="1.0.0",
    description="API for user authentication and management."
)

@app.on_event("startup")
async def startup_event():
    await init_postgres_pool()

    print("Ứng dụng đã khởi động và kết nối DB.")


@app.on_event("shutdown")
async def shutdown_event():
    """Xử lý sự kiện khi ứng dụng dừng: Đóng kết nối DB."""

    # 1. Đóng kết nối PostgreSQL
    await close_postgres_pool()

    print("Ứng dụng đã dừng.")


# ----------------- KẾT NỐI ROUTER (API Endpoints) -----------------

# 1. Import và kết nối router User
# Đảm bảo bạn đã tạo file routers/user.py (chưa được cung cấp)
try:
    from routers.user import user_router

    app.include_router(user_router, prefix="/users", tags=["Users"])
except ImportError:
    print("WARNING: Không tìm thấy routers/user.py. API endpoints không khả dụng.")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Chào mừng đến với Capstone API. Truy cập /docs để xem tài liệu."}

# ----------------- CÁCH CHẠY -----------------
# Chạy ứng dụng bằng lệnh Terminal:
# uvicorn main:app --reload