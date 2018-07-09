import hashlib

class HashGenerator:
    @staticmethod
    def md5HashGenerator(password= str()):
        print(password)
        return hashlib.md5(password.encode("utf-8")).hexdigest()
