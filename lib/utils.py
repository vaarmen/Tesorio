import os
import re
import random
import hashlib
import logging
import string
import unicodedata
from datetime import datetime, timedelta
import Cookie
import webapp2

from google.appengine.api import memcache

## For generate_company_map()
from models import Company

def generate_company_map():
    """Generates Company ID -> Company Name dictionary"""
    companies = Company.query()
    company_map = {}

    for company in companies:
        logging.info(dir(company))
        company_map[str(company.key.id())] = company.name

    memcache.set('company_map', company_map)

    return company_map


def random_string(size=6, chars=string.ascii_letters + string.digits):
    """ Generate random string """
    return ''.join(random.choice(chars) for _ in range(size))

def hashing(plaintext, salt="", sha="512"):
    """ Returns the hashed and encrypted hexdigest of a plaintext and salt"""
    app = webapp2.get_app()

    # Hashing
    if sha == "1":
        phrase = hashlib.sha1()
    elif sha == "256":
        phrase = hashlib.sha256()
    else:
        phrase = hashlib.sha512()
    phrase.update("%s@%s" % (plaintext, salt))
    phrase_digest = phrase.hexdigest()

    # Encryption (PyCrypto)
    try:
        from Crypto.Cipher import AES

        mode = AES.MODE_CBC

        # We can not generate random initialization vector because is difficult to retrieve them later without knowing
        # a priori the hash to match. We take 16 bytes from the hexdigest to make the vectors different for each hashed
        # plaintext.
        iv = phrase_digest[:16]
        encryptor = AES.new(app.config.get('aes_key'), mode, iv)
        ciphertext = [encryptor.encrypt(chunk) for chunk in chunks(phrase_digest, 16)]
        return ''.join(ciphertext)
    except Exception, e:
        logging.error("CRYPTO is not running: {}".format(e))
        raise

def chunks(list, size):
    """ Yield successive sized chunks from list. """

    for i in xrange(0, len(list), size):
        yield list[i:i + size]

def encode(plainText):
    num = 0
    key = "0123456789abcdefghijklmnopqrstuvwxyz"
    key += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for c in plainText: num = (num << 8) + ord(c)
    encodedMsg = ""
    while num > 0:
        encodedMsg = key[num % len(key)] + encodedMsg
        num /= len(key)
    return encodedMsg


def decode(encodedMsg):
    num = 0
    key = "0123456789abcdefghijklmnopqrstuvwxyz"
    key += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for c in encodedMsg: num = num * len(key) + key.index(c)
    text = ""
    while num > 0:
        text = chr(num % 256) + text
        num /= 256
    return text

def write_cookie(cls, COOKIE_NAME, COOKIE_VALUE, path, expires=7200):
    """
    Write a cookie
    @path = could be a cls.request.path to set a specific path
    @expires = seconds (integer) to expire the cookie, by default 2 hours ()
    expires = 7200 # 2 hours
    expires = 1209600 # 2 weeks
    expires = 2629743 # 1 month
    """

    # days, seconds, then other fields.
    time_expire = datetime.now() + timedelta(seconds=expires)
    time_expire = time_expire.strftime("%a, %d-%b-%Y %H:%M:%S GMT")

    cls.response.headers.add_header(
        'Set-Cookie',
        COOKIE_NAME + '=' + COOKIE_VALUE + '; expires=' + str(time_expire) + '; path=' + path + '; HttpOnly')
    return

def read_cookie(cls, name):
    """ Use: cook.read(cls, COOKIE_NAME) """

    string_cookie = os.environ.get('HTTP_COOKIE', '')
    cls.cookie = Cookie.SimpleCookie()
    cls.cookie.load(string_cookie)
    value = None
    if cls.cookie.get(name):
        value = cls.cookie[name].value

    return value