from lib.databases.crud import CRUD
from lib.databases.dao import DAO
import time
import hashlib
import random
import os
from random_word import RandomWords

###
### This class authenticates user requests against database records.
###

class Authenticator(DAO):
    def __init__(self):
        self.random_words = RandomWords()
        self.EXPIRY = 1800 # seconds
    
    def is_session_expired(self, token):
        session = self.get_session(token)
        if not "expiry" in session:
            return True
        if int(time.time()) >= int(session["expiry"]) + self.EXPIRY:
            return True
        print(session["expiry"])
        print(time.time())
        return False
    
    def is_user_admin(self, user_ID):
        user_record = self.get_user(_user_ID = user_ID)
        if not "isAdmin" in user_record:
            return False
        if bool(user_record["isAdmin"]):
            return True
        return False
    
    def is_user_logged(self, user_ID):
        session = self.get_session(user_ID=user_ID)
        if not "user_ID" in session:
            return False
        if session["user_ID"] is not None:
            return True
        return False
    
    def generateSessionToken(self):
        randomBytes = os.urandom(32)
        sha256 = hashlib.sha256(randomBytes)
        return sha256.hexdigest()

    ### Encrypt the hash root and return it as token.
    def generate_hash(self):
        hash_root = self.get_hash_root()
        combinedBytes = hash_root
        hashedBytes = hashlib.sha256(combinedBytes)
        return hashedBytes.hexdigest()
    
    ### Generate hash root without user signature.
    ### Signature is stored in session record instead.
    def get_hash_root(self):
        hash_root = self.random_words.get_random_word()
        index = random.randint(0, len(hash_root) - 1)
        replacement = str(random.randint(0, 6969)) 
        hash_root = hash_root[:index] + replacement + hash_root[index + 1:]
        hash_root += str(random.randint(0, 999))
        return hash_root.encode("utf-8")
    
    def areCredsValid(self, enteredHash):
        allUsers = self.read("users", "Users")
        for username, password, storedHash in allUsers:
            if (enteredHash == storedHash):
                return True
        return False
