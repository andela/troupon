from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from hashids import Hashids
from time import time

from troupon.settings import SECRET_KEY as secret_key


class UserHasher:
    """ NOTE: This class has the Hashids package as a dependency.
        Run 'pip install requirements.txt' to install on your environment. """

    timehash_min_length = 40
    pkhash_min_length = 20
    alphabet = 'abcdefghijklmnopqrstuvwyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    delim = "x"

    @staticmethod
    def gen_hash(registered_user):
        """ accepts a intsance of user account and returns a reversible 'time-unique' hash for it """

        # get a timestamp (to make each generated hash unique):
        timestamp = int(time() * 1000)

        # encode the timestamp with secret_key:
        hashids = Hashids(salt=secret_key, min_length=UserHasher.timehash_min_length, alphabet=UserHasher.alphabet)
        timestamp_hash = hashids.encode(timestamp)

        # encode the user's pk with timestamp:
        hashids = Hashids(salt=str(timestamp), min_length=UserHasher.pkhash_min_length, alphabet=UserHasher.alphabet)
        pk_hash = hashids.encode(registered_user.pk)

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

        try:
            # decode the timestamp_hash (i.e hashs[0] ) with the app secret key:
            hashids = Hashids(salt=secret_key, min_length=UserHasher.timehash_min_length, alphabet=UserHasher.alphabet)
            timestamp = hashids.decode(hashs[0])[0]

            # decode the pk_hash (i.e hashs[1] ) with the timestamp:
            hashids = Hashids(salt=str(timestamp), min_length=UserHasher.pkhash_min_length, alphabet=UserHasher.alphabet)
            account_pk = hashids.decode(hashs[1])[0]

            # return the account for that pk if it exists:
            registered_user = User.objects.get(pk=account_pk)
            return registered_user

        except:
            # return None if it doesn't:
            return None
