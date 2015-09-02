from hashids import Hashids
from time import time
from troupon.settings import SECRET_KEY as secret_key


def gen_user_hash(
    user_account, 
    timeshash_min_length=15, 
    userhash_min_length=35, 
    alphabet='abcdefghijklmnopqrstuvwxyz0123456789', 
    delim="_"):

    # get a hashed timestamp (to make each generated hash unique):
    hashids = Hashids(salt=secret_key, min_length=timeshash_min_length, alphabet=alphabet)
    time_stamp_hash = hashids.encode(int(time() * 1000))

    # use it to hash the user('email'):
    hashids = Hashids(salt=time_stamp_hash, min_length=userhash_min_length, alphabet=alphabet)
    user_hash = hashids.encode(user_account.email)

    # return the combination delimited by delim:
    return "%s%s%s" % (user_hash, delim, time_stamp_hash)
