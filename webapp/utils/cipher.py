import base64
import hashlib

from cryptography.fernet import Fernet, InvalidToken


class Cipher:
    def __init__(self, secret):
        self.cipher_suite = Fernet(
            base64.urlsafe_b64encode(
                hashlib.sha256(secret.encode("utf-8")).digest()
            )
        )

    def encrypt(self, raw_text):
        return self.cipher_suite.encrypt(
            bytes(raw_text.encode("utf-8"))
        ).decode("utf-8")

    def decrypt(self, token):
        try:
            return self.cipher_suite.decrypt(
                bytes(token.encode("utf-8"))
            ).decode("utf-8")
        except InvalidToken:
            return None
