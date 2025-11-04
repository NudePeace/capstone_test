from AuthUtil import hash_password
from Model.UserModel import UserRegisterRequest, UserLoginRequest
from Database import execute_query

async def register_new_user(user_data: UserRegisterRequest) -> int:

    hashed_password = hash_password(user_data.password)
    sql_account_query = """
    INSERT INTO users (username, email, password)
    VALUES ($1, $2, $3)
    RETURNING user_id;
    """
    try:
        user_id = await execute_query(sql_account_query,
                                             user_data.username,
                                             user_data.email,
                                             hashed_password)
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise Exception("계정 생성 중 오류가 발생했습니다")

    sql_profile_query = """
    INSERT INTO user_info (user_id, name, phone_number, date_of_birth, gender, address)
    VALUES ($1, $2, $3, $4, $5, $6);
    """

    try:
        await execute_query(sql_profile_query,
                            user_id,
                            user_data.name,
                            user_data.phone_number,
                            user_data.date_of_birth,
                            user_data.gender,
                            user_data.address)
    except ValueError as e:
        await execute_query("DELETE FROM users WHERE user_id = $1;", user_id)
        raise ValueError("휴대폰 번호가 등록되었습니다")
    except Exception as e:
        await execute_query("DELETE FROM users WHERE user_id = $1;", user_id)
        raise Exception("사용자 프로필을 생성하는 과정 오류가 발생했습니다.")

    return user_id

async def login(user_data: UserLoginRequest) -> AccessToken:
    try:
        sql_query = """
            SELECT user_id, password, email FROM users
            WHERE email = $1;
            """
        user_record = await execute_query(sql_query, user_data.email)
    except e