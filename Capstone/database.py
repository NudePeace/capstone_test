# File: database.py

from motor.motor_asyncio import AsyncIOMotorClient
import asyncpg
from typing import Any, Optional
import os

# Lưu ý: Cần đảm bảo load_dotenv() đã được gọi ở đầu file main.py

# ----------------- LẤY CẤU HÌNH TỪ BIẾN MÔI TRƯỜNG -----------------

# PostgreSQL
# Sử dụng POSTGRES_URL từ .env
POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://default:default@localhost:5432/test")
# Lấy tên DB nếu cần để đảm bảo đồng bộ
POSTGRES_DB_NAME = os.getenv("POSTGRES_DB", "capstone")

# MongoDB
# Sử dụng MONGO_URL từ .env (bao gồm cả host, user, pass và authSource)
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
# Lấy tên DB
MONGO_DB_NAME = os.getenv("MONGO_DB", "capstone")

# ----------------- CẤU HÌNH POSTGRESQL (asyncpg) -----------------

# Pool kết nối PostgreSQL toàn cục
db_postgres: Optional[asyncpg.Pool] = None


async def init_postgres_pool():
    """Khởi tạo pool kết nối PostgreSQL."""
    global db_postgres
    try:
        db_postgres = await asyncpg.create_pool(POSTGRES_URL)
        print("PostgreSQL: Kết nối pool thành công.")
    except Exception as e:
        print(f"Lỗi kết nối PostgreSQL: {e}")
        # Xử lý lỗi kết nối: có thể raise hoặc exit ứng dụng


async def close_postgres_pool():
    """Đóng pool kết nối PostgreSQL."""
    if db_postgres:
        await db_postgres.close()
        print("PostgreSQL: Đã đóng pool kết nối.")


# ----------------- CẤU HÌNH MONGODB (motor) -----------------

CLIENT = AsyncIOMotorClient(MONGO_URL)
db_mongo = CLIENT[MONGO_DB_NAME]  # Sử dụng tên database từ biến môi trường

async def check_mongo_connection():
    """Kiểm tra kết nối MongoDB."""
    try:
        # Lệnh kiểm tra kết nối đơn giản
        await db_mongo.client.server_info()
        print("MongoDB: Kết nối thành công.")
    except Exception as e:
        print(f"Lỗi kết nối MongoDB: {e}")
        # Xử lý lỗi kết nối tại đây


# ----------------- HÀM THỰC THI SQL -----------------

async def execute_query(query: str, *args: Any) -> int:
    """
    Thực thi query SQL và trả về ID vừa được tạo (hoặc 0 nếu không có ID).
    Tối ưu cho việc bắt lỗi Unique Violation khi đăng ký.
    """
    if not db_postgres:
        raise ConnectionError("PostgreSQL pool chưa được khởi tạo. Kiểm tra sự kiện 'startup' trong main.py.")

    try:
        # Sử dụng 'fetchval' để lấy giá trị đầu tiên (ID)
        new_id = await db_postgres.fetchval(query, *args)

        return new_id if new_id is not None else 0

    except asyncpg.exceptions.UniqueViolationError:
        # Bắt lỗi nếu username/email bị trùng
        raise ValueError("Tài khoản đã tồn tại: Username hoặc Email đã được sử dụng.")
    except Exception as e:
        # Bắt các lỗi SQL khác
        print(f"Lỗi thực thi SQL: {e}")
        raise Exception("Đã xảy ra lỗi trong quá trình thao tác cơ sở dữ liệu.")