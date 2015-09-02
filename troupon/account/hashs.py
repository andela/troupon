from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User as Account

from hashids import Hashids
from time import time

from troupon.settings import SECRET_KEY as secret_key

class UserHashUtils:
    """ NOTE: This class has the Hashids package as a dependency. 
        Run 'pip install requirements.txt' to install on your environment. """

    timehash_min_length = 15
    userhash_min_length = 35
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    delim = "_"

    @staticmethod
    def gen_hash(user_account):
        """ accepts a intance of user account and returns a reversible 'time-unique' hash for it """

        # get a timestamp (to make each generated hash unique):
        timestamp = int(time() * 1000)

        # encode the timestamp with secret_key:
        hashids = Hashids(salt=secret_key, min_length=UserHashUtils.timehash_min_length, alphabet=UserHashUtils.alphabet)
        timestamp_hash = hashids.encode(int(time() * 1000))

        # encode the user's email with timestamp:
        hashids = Hashids(salt=str(timestamp), min_length=UserHashUtils.userhash_min_length, alphabet=UserHashUtils.alphabet)
        user_email_hash = hashids.encode(user_account.email)

        # return the combination delimited by UserHashUtils.delim:
        return "%s%s%s" % (user_email_hash, UserHashUtils.delim, timestamp_hash)

    @staticmethod
    def reverse_hash(hash_str):
        """ accepts a unique hash string representing a user account and decodes it to return an actual intance of that account
            Returns None if decoded user does not exits """

        # split the hash_str with the delim:
        hash_list = hash_str.split(UserHashUtils.delim)

        # ensure the list has only 2 parts 
        if len(hash_list) != 2:
            return None

        # decode the timestamp_hash (i.e hash_list[1] ) with the app secret key:
        hashids = Hashids(salt=secret_key, min_length=UserHashUtils.timehash_min_length, alphabet=UserHashUtils.alphabet)
        timestamp = hashids.decode(hash_list[1])

        # decode the user_email_hash (i.e hash_list[0] ) with the timestamp:
        hashids = Hashids(salt=str(timestamp), min_length=UserHashUtils.timehash_min_length, alphabet=UserHashUtils.alphabet)
        user_email = hashids.decode(hash_list[0])

        try:
            # retrun the account for that email if it exists:
            registered_account = Account.objects.get(email__exact=user_email)
            return registered_account
            
        except ObjectDoesNotExist:
             # return None if it doesn't:
            return None