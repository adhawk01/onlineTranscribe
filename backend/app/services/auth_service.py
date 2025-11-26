import app.services.user_service as user_service
from app.utils.auth_utils import hash_password, verify_password, generate_token, decode_token


def register_user(email: str, username: str, password: str, account_type: str = "user"):
    # Check if email is already taken
    if user_service.get_user_by_email(email):
        raise ValueError("Email already registered.")

    # Check if username is already taken
    if user_service.get_user_by_username(username):
        raise ValueError("Username already taken.")

    # Hash the password
    password_hashed = hash_password(password)

    # Create the user
    success = user_service.create_user(
        user_email=email,
        user_name=username,
        hashed_password=password_hashed,
        account_type=account_type
    )

    if not success:
        raise Exception("Failed to create user.")

    return {"message": "User registered successfully."}


def login_user(email: str, password: str):
    # Get user by email
    user = user_service.get_user_by_email(email)

    if not user:
        raise ValueError("Invalid email or password.")

    # user = [(id, user_email, user_password, user_name, user_account_type)]
    user = user[0]
    user_id, user_email, user_password_hash, user_name, account_type = user

    # Verify password
    if not verify_password(password, user_password_hash):
        raise ValueError("Invalid email or password.")

    # Generate JWT token
    token = generate_token(user_id)

    return {
        "token": token,
        "user": {
            "id": user_id,
            "email": user_email,
            "username": user_name,
            "account_type": account_type
        }
    }
