"""Сервис для работы с паролями.

Этот модуль предоставляет утилиты для хеширования и проверки паролей
с использованием SHA-256 хеширования.

Classes:
    PasswordService: Статический класс с методами для работы с паролями
    
Note:
    В production среде рекомендуется использовать более безопасные
    алгоритмы хеширования, такие как bcrypt или Argon2.
"""

import hashlib


class PasswordService:
    """Сервис для хеширования и проверки паролей.
    
    Предоставляет статические методы для работы с паролями без необходимости
    создания экземпляра класса.
    
    Methods:
        hash_password(password): Хеширует пароль с использованием SHA-256
        verify_password(plain_password, hashed_password): Проверяет соответствие пароля хешу
        
    Example:
        >>> from app.service.password_service import PasswordService
        >>> 
        >>> # Хеширование пароля
        >>> hashed = PasswordService.hash_password("my_secret_password")
        >>> print(hashed)
        '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'
        >>> 
        >>> # Проверка пароля
        >>> is_valid = PasswordService.verify_password("my_secret_password", hashed)
        >>> print(is_valid)
        True
        
    Warning:
        SHA-256 без salt не является безопасным для production!
        Используйте bcrypt, scrypt или Argon2 для реальных приложений.
    """
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Проверка соответствия пароля хешу.
        
        Хеширует предоставленный пароль и сравнивает с сохраненным хешем.
        
        Args:
            plain_password (str): Пароль в открытом виде
            hashed_password (str): Хешированный пароль для сравнения
            
        Returns:
            bool: True если пароли совпадают, False в противном случае
            
        Example:
            >>> PasswordService.verify_password("password123", "hashed_password")
            False
        """
        return PasswordService.hash_password(plain_password) == hashed_password

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Хеширование пароля с использованием SHA-256.
        
        Преобразует пароль в SHA-256 хеш в шестнадцатеричном формате.
        
        Args:
            password (str): Пароль в открытом виде
            
        Returns:
            str: Хеш пароля в шестнадцатеричном формате (64 символа)
            
        Example:
            >>> PasswordService.hash_password("secret")
            '2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b'
            
        Security Note:
            Эта реализация НЕ использует salt и не является безопасной!
            Для production используйте:
            - bcrypt: from passlib.hash import bcrypt
            - Argon2: from passlib.hash import argon2
            - scrypt: from passlib.hash import scrypt
        """
        return hashlib.sha256(password.encode()).hexdigest()