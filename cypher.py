from Crypto.Cipher import AES

class Cypher:

    def __init__(self, key, size_block=16):
        self.size_block = size_block
        self.key = self.pad(key)
        self.cypher = AES.new(self.key)

    def pad(self, text):
        return text + '}'*(self.size_block - (len(text) % self.size_block))

    def unpad(self, text):
        return text.replace('}','')

    def encrypt(self, msg):
        return self.cypher.encrypt(self.pad(msg))

    def decrypt(self,msg):
        return self.unpad(self.cypher.decrypt(msg).decode('utf-8'))
