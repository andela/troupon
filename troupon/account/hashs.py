from django.contrib.auth.models import User as Account
from django.core.exceptions import ObjectDoesNotExist

from hashids import Hashids
from time import time

from troupon.settings import SECRET_KEY as secret_key


class UserHasher:
    """ NOTE: This class has the Hashids package as a dependency. 
        Run 'pip install requirements.txt' to install on your environment. """

    timehash_min_length = 40
    userhash_min_length = 20
    alphabet = 'abcdefghijklmnopqrstuvwyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    delim = "x"

    @staticmethod
    def gen_hash(registered_account):
        """ accepts a intsance of user account and returns a reversible 'time-unique' hash for it """
        
        # get a timestamp (to make each generated hash unique):
        timestamp = int(time() * 1000)

        # encode the timestamp with secret_key:
        hashids = Hashids(salt=secret_key, min_length=UserHasher.timehash_min_length, alphabet=UserHasher.alphabet)
        timestamp_hash = hashids.encode(timestamp)
        
        # encode the user's pk with timestamp:
        hashids = Hashids(salt=str(timestamp), min_length=UserHasher.userhash_min_length, alphabet=UserHasher.alphabet)
        pk_hash = hashids.encode(registered_account.pk)
        
        # return the combination delimited by UserHasher.delim:
        return "%s%s%s" % (timestamp_hash, UserHasher.delim, pk_hash)


    @staticmethod
    def reverse_hash(hash_str):
        """ accepts a unique hash string representing a user account and decodes it to return an actual intance of that account
            Returns None if decoded user does not exits """

        # split the hash_str with the delim:
        hashs = hash_str.split(UserHasher.delim)
        
        # ensure the list has only 2 parts 
        if len(hashs) != 2:
            return None

        # decode the timestamp_hash (i.e hashs[0] ) with the app secret key:
        hashids = Hashids(salt=secret_key, min_length=UserHasher.timehash_min_length, alphabet=UserHasher.alphabet)
        timestamp = hashids.decode(hashs[0])[0]
        
        # decode the pk_hash (i.e hashs[1] ) with the timestamp:
        hashids = Hashids(salt=str(timestamp), min_length=UserHasher.userhash_min_length, alphabet=UserHasher.alphabet)
        account_pk = hashids.decode(hashs[1])[0]
        
        try:
            # return the account for that pk if it exists:
            registered_account = Account.objects.get(pk=account_pk)
            return registered_account
        except ObjectDoesNotExist:
            # return None if it doesn't:
            return None