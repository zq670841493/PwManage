import base64
 
from Crypto.Cipher import AES
 
 
# 补足字符串长度为16的倍数
def add_to_16(s):
    while len(s) % 16 != 0:
        s += '\0'
    return str.encode(s)  # 返回bytes

#加密
def encrypted(pw,key1):
	key2='Jd2U%$r56uOi8mF05bvO980pZJ'
	key=key1+key2   # 密钥长度必须为16、24或32位，分别对应AES-128、AES-192和AES-256
	aes = AES.new(str.encode(key), AES.MODE_ECB)  # 初始化加密器，本例采用ECB加密模式
	encrypted_text = str(base64.encodebytes(aes.encrypt(add_to_16(pw))), encoding='utf8').replace('\n', '')  # 加密
	return encrypted_text

#解密
def decrypted(pw,key1):
	key2='Jd2U%$r56uOi8mF05bvO980pZJ'
	key=key1+key2   # 密钥长度必须为16、24或32位，分别对应AES-128、AES-192和AES-256
	try:
		aes = AES.new(str.encode(key), AES.MODE_ECB)  # 初始化加密器，本例采用ECB加密模式	
		decrypted_text = str(aes.decrypt(base64.decodebytes(bytes(pw, encoding='utf8'))).rstrip(b'\0').decode("utf8"))  # 解密
		return decrypted_text
	except :
		return '解密失败'

	

if __name__ == '__main__':
	pw='d3178f32a166ab63b'
	key1='123466'
	a=encrypted(pw,key1)
	print(a)
	pw=a
	b=decrypted(pw,key1)
	print(b)
	