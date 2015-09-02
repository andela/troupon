# from hashids import Hashids
# from time import time
# from troupon.settings import SECRET_KEY as secret_key


# def gen_user_hash(user_account, min_length=50, alphabet='abcdefghijklmnopqrstuvwxyz0123456789'):
	
#     hashids = Hashids(salt=user_account, min_length=min_length, alphabet=alphabet)
#     uid = hashids.encode(int(time() * 1000)).upper()
#     return uid