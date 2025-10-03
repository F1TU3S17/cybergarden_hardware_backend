import hashlib

class PasswordService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return PasswordService.hash_password(plain_password) == hashed_password

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()