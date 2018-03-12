# -*- coding:utf-8 -*-
import random
#最大公因數
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi
    
    while e > 0:
        temp1 = temp_phi/e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        
        x = x2- temp1 * x1
        y = d - temp1 * y1
        
        x2 = x1
        x1 = x
        d = y1
        y1 = y
    
    if temp_phi == 1:
        return d + phi


#確認是否為質數
def is_prime(num):
    if num == 2:
        return True
    #1和能被2除的不是質數，所以濾除
    if num < 2 or num % 2 == 0:
        return False

    #將num開根號+2, 每個數字間隔2(找出3~num之間的所有質數)    
    for n in xrange(3, int(num**0.5)+2, 2):
        #確認num也不能被中間的質數整除
        if num % n == 0:
            return False
    return True

def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        print ('Both numbers must be prime.')
    elif p == q:
        print ('p and q cannot be equal')
    #n = pq
    n = p * q

    #Phi = (p-1) * (q-1)
    phi = (p-1) * (q-1)

    #選擇一個整數e，e和phi（n）是互質的
    e = random.randrange(1, phi)

    #使用歐幾里德算法驗證e和phi（n）是互質的
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    #使用擴展歐幾里得算法來生成私鑰
    d = multiplicative_inverse(e, phi)
    
    #回傳產生的公鑰and私鑰
    #公鑰 = (e, n) , 私鑰 = (d, n)
    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    key, n = pk
    #使用a^b mod m將明文中的每個字母轉換為基於字符的數字
    cipher = [(ord(char) ** key) % n for char in plaintext]
    #回傳list[bytes]
    return cipher

def decrypt(pk, ciphertext):
    key, n = pk
    #使用a^b mod m生成基於密文和密鑰的明文
    plain = [chr((char ** key) % n) for char in ciphertext]
    #回傳str[bytes]
    return ''.join(plain)
    

if __name__ == '__main__':
    print "RSA Encrypter/ Decrypter"
    p = int(raw_input("請輸入質數 (17, 19, 23, etc): "))
    q = int(raw_input("再輸入一次質數(請勿重複): "))
    print "產生您的 public/private中 . . ."
    public, private = generate_keypair(p, q)
    print "您的 public key ", public ," / 與 private key ", private
    message = raw_input("請輸入訊息(以私鑰加密): ")
    encrypted_msg = encrypt(private, message)
    print "加密後的訊息為: "
    print ''.join(map(lambda x: str(x), encrypted_msg))
    print "使用公鑰來解開訊息 ", public ," . . ."
    print "解開後的訊息為:"
    print decrypt(public, encrypted_msg)