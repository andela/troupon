import os

from django.contrib.auth.models import User

from hashids import Hashids
from time import time


class UserHasher:
    """
    NOTE: This class has the Hashids package as a dependency.
    Run 'pip install requirements.txt' to install on your environment.

    Attributes:
        timehash_min_length: An integer representing the minimum
            length of the generated time hash.
        pkhash_min_length: An integer representing the minimum
            length of the primary key hash.
        alphabet: A string representing available characters to construct
            hash from.
        delim: A string representing the delimiter to be used to
            concatenate the generated time hash and primary key hash.
    """

    timehash_min_length = 40
    pkhash_min_length = 20
    alphabet = 'abcdefghijklmnopqrstuvwyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    delim = "x"
    # from settings.py
    secret_key = os.getenv('SECRET_KEY')

    @staticmethod
    def gen_hash(registered_user):
        """Generates a time dependent hash.

        Accepts an instance of user account and returns
        a reversible 'time-unique' hash for it.

        Args:
            registered_user: A user instance.
        Returns:
            A hash composed of a time-stamp hash and a
            pk-hash delimited by x.
        """

        # get a timestamp (to make each generated hash unique):
        timestamp = int(time() * 1000)

        # encode the timestamp with secret_key:
        hashids = Hashids(
            salt=UserHasher.secret_key,
            min_length=UserHasher.timehash_min_length,
            alphabet=UserHasher.alphabet
        )
        timestamp_hash = hashids.encode(timestamp)

        # encode the user's pk with timestamp:
        hashids = Hashids(
            salt=str(timestamp),
            min_length=UserHasher.pkhash_min_length,
            alphabet=UserHasher.alphabet
        )
        pk_hash = hashids.encode(registered_user.pk)

        # return the combination delimited by UserHasher.delim:
        return "%s%s%s" % (timestamp_hash, UserHasher.delim, pk_hash)

    @staticmethod
    def reverse_hash(hash_str):
        """Reverses a hash parsed from the request URL.

        Accepts a unique hash string representing a user account
        and decodes it to return an actual intance of that account.

        Args:
            hash_str: an hash string.
        Returns:
            None if decoded user does not exist.
            user instance if decoded user exists.
        """

        # split the hash_str with the delim:
        hashs = hash_str.split(UserHasher.delim)

        # ensure the list has only 2 parts
        if len(hashs) != 2:
            return None

        try:
            # decode the timestamp_hash (i.e hashs[0] )
            # with the app secret key:
            hashids = Hashids(
                salt=UserHasher.secret_key,
                min_length=UserHasher.timehash_min_length,
                alphabet=UserHasher.alphabet
            )
            timestamp = hashids.decode(hashs[0])[0]

            # decode the pk_hash (i.e hashs[1] ) with the timestamp:
            hashids = Hashids(
                salt=str(timestamp),
                min_length=UserHasher.pkhash_min_length,
                alphabet=UserHasher.alphabet
            )
            account_pk = hashids.decode(hashs[1])[0]

            # return the account for that pk if it exists:
            registered_user = User.objects.get(pk=account_pk)
            return registered_user

        except:
            # return None if it doesn't:
            return None
