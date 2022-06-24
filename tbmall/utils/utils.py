from Crypto.Cipher import AES
from Crypto import Random

class Cryptog:

    def resize_length(s):
        '''
        将明文的长度修改为16的倍数（在创建cipher时会用到）
        '''
        return s.rjust((len(s) // 16 + 1) * 16)

    def encrypt(s, cipher: AES):
        ciphered_bytes = cipher.encrypt(Cryptog.resize_length(s).encode())
        ciphertext = ''.join(['{:02x}'.format(c) for c in ciphered_bytes]) # 将bytes转换到hex格式
        return ciphertext

    def decrypt(s, cipher: AES):
        ciphered_bytes = bytes.fromhex(s) # 将hex字符串转回bytes
        return cipher.decrypt(ciphered_bytes).decode().lstrip()

    def gen_cipher():
        # iv = Random.new().read(AES.block_size)
        # key 和 iv的长度需要为16 bytes
        key = 'This is a key123' 
        iv = 'This is an iv234'
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return cipher
    
    def decrypt_encoded_info(info):
        # todo
        # 先读取加密后数据和之前用于加密数据的cipher，解密出原始数据，再将原始数据用新生成的随机cipher加密，同时保存密文和cipher，提升安全性
        cipher = Cryptog.gen_cipher()
        return Cryptog.decrypt(info, cipher)
