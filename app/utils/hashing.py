import bcrypt


class Hash:
    @staticmethod
    def hash(password: str) -> str:
        """
        Hash a password with bcrypt.
        """
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        return hashed_password.decode('utf-8')

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        """
        Verify the provided password against the hashed password.
        """
        password_byte_enc = plain_password.encode('utf-8')
        return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password.encode('utf-8'))
