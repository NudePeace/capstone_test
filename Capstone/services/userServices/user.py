# Import logic hash mật khẩu
from auth_utils import hash_password

# Import mô hình Pydantic
from models.user import UserRegisterRequest

# Import hàm thực thi query từ database.py.
# CHỈ CẦN IMPORT execute_query
from database import execute_query

async def register_new_user(user_data: UserRegisterRequest) -> int:
    """
    Thực hiện logic đăng ký: hash pass và LƯU TẤT CẢ VÀO POSTGRESQL (Tạm thời).
    """

    # 1. HASH MẬT KHẨU
    hashed_password = hash_password(user_data.password)

    # 2. LƯU THÔNG TIN ACCOUNT VÀ PROFILE VÀO POSTGRESQL (GIẢ ĐỊNH CÓ BẢNG user_profile)

    # **GIAI ĐOẠN A: TẠO ACCOUNT**
    sql_account_query = """
    INSERT INTO account (username, email, password)
    VALUES ($1, $2, $3)
    RETURNING account_id;
    """

    try:
        new_account_id = await execute_query(sql_account_query,
                                             user_data.username,
                                             user_data.email,
                                             hashed_password)
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise Exception("Đã xảy ra lỗi trong quá trình tạo tài khoản.")

    # **GIAI ĐOẠN B: TẠO USER PROFILE**
    # Tạm thời lưu profile vào bảng SQL user_profile
    # Bạn cần đảm bảo bảng user_profile có các cột: account_id (FK), first_name, last_name, v.v.
    sql_profile_query = """
    INSERT INTO user_profile (account_id, name, phone_number, date_of_birth, gender, address)
    VALUES ($1, $2, $3, $4, $5, $6);
    """

    try:
        # Không cần trả về ID vì nó dùng khóa ngoại (account_id)
        await execute_query(sql_profile_query,
                            new_account_id,
                            user_data.name,
                            user_data.phone_number,
                            user_data.date_of_birth,
                            user_data.gender,
                            user_data.address)
    except Exception as e:
        # Xử lý trường hợp lỗi khi tạo profile (cần rollback account ở trên, nhưng ta bỏ qua tạm thời)
        raise Exception("Đã xảy ra lỗi khi tạo hồ sơ người dùng.")

    # 4. TRẢ VỀ ID
    return new_account_id