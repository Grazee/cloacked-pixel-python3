import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes

'''
Thanks to
http://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256
'''
class AESCipher:
    def __init__(self, key):
        self.bs = 32	# Block size
        self.key = hashlib.sha256(key.encode()).digest()	# 32 bit digest

    def encrypt(self, raw):
        raw = self.pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(raw)

    def decrypt(self, enc):
        # if len(enc) % 16 != 0:
        #     enc = enc[:len(enc) - len(enc)%16]
        # print(len(enc))
        iv = enc[:AES.block_size]        
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        message = cipher.decrypt(enc[AES.block_size:])

        return message
        # return self.unpad()

    def pad(self, s):
        return s + (self.bs - len(s) % self.bs) * long_to_bytes(self.bs - len(s) % self.bs)

    def unpad(self, s):
        return s[:-ord(s[len(s)-1:])]
