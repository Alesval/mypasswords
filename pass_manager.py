from cypher import Cypher
import shelve
import secrets
import hashlib

FILENAME = 'passwords'
PASS_FIELD = 'pass'
TOKEN_FIELD = 'token'

class PassManagerException(Exception):
    pass

class PassManager:


    def __init__(self):
        self.file = shelve.open(FILENAME)


    def __del__(self):
        self.file.close()


    def auth_access(self, key):
        try:
            stored_pass = self.file[PASS_FIELD]
            token = self.file[TOKEN_FIELD]
            if stored_pass == self.__hash(key, token):
                self.key = key
                self.cypher = Cypher(self.key)
                return True
            else:
                raise PassManagerException('Wrong Key')
        except KeyError:
            self.key = key
            self.cypher = Cypher(self.key)
            token = self.__generate_key()
            self.file[TOKEN_FIELD] = token
            self.file[PASS_FIELD] = self.__hash(self.key,token)
            return True


    def get_services(self):
        if not self.key:
            raise PassManagerException("You need to authenticate first")
        elif (len(self.file.keys()) - 2) > 0:
            return [elem for elem in self.file if elem != PASS_FIELD and elem != TOKEN_FIELD]
        else:
            raise PassManagerException("There aren't saved services yet")


    def remove_service(self, service):
        if not self.key:
            raise PassManagerException("You need to authenticate first")
        elif service != PASS_FIELD and service != TOKEN_FIELD:
            try:
                del self.file[service]
                return True
            except KeyError:
                raise PassManagerException('Service not found')
        else:
            raise PassManagerException('Service not found')
        return False


    def add_pass(self, service, passwd):
        if not self.key:
            raise PassManagerException("You need to authenticate first")
        elif service != PASS_FIELD and service != TOKEN_FIELD:
            try:
                var = self.file[service]
                if var:
                    raise PassManagerException('This service already exists. Remove it if you want to change the password')
            except KeyError:
                self.file[service] = self.cypher.encrypt(passwd)
                return True
        else:
            raise PassManagerException("that service name can't be used, sorry")


    def retrieve_pass(self, service):
        if not self.key:
            raise PassManagerException("You need to authenticate first")
        elif service != PASS_FIELD and service != TOKEN_FIELD:
            try:
                passwd = self.cypher.decrypt(self.file[service])
                return passwd
            except KeyError:
                raise PassManagerException("Service not found")
        else:
            raise PassManagerException("Service not found")


    def __generate_key(self):
        return secrets.token_bytes(20)


    def __hash(self, key, random_token):
        return hashlib.sha224(key.encode('utf-8') + random_token).hexdigest()
