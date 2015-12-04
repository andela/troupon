from binascii import unhexlify
from django_otp.models import Device
from django_otp.oath import totp
import time
from django_otp.util import random_hex, hex_validator
from django.db import models


class CustomTOTPDevice(Device):

    '''Device Model Object defined to generate Token Key for Merchants. '''

    key = models.CharField(max_length=80,
                           validators=[hex_validator()],
                           default=lambda: random_hex(20),
                           help_text=u'A hex-encoded secret key of up to 40 bytes.')

    last_t = models.BigIntegerField(
        default=-1,
        help_text="The t value of the latest verified token. The next token must be at a higher time step."
    )


    @property
    def bin_key(self):
        return unhexlify(self.key)

    @staticmethod
    def generate_token(self): 
        totp = self.totp_obj()
        token = format(totp.token(), '06d')

        return token

    @staticmethod
    def verify_token(self, token):
        try:
            token = int(token)
        except Exception:
            verified = False
        else:
            totp = self.totp_obj()
            tolerance = settings.CUSTUM_OTP_TOKEN_VALIDITY

            for offset in range(-tolerance, 1):
                totp.drift = offset
                if (totp.t() > self.last_t) and (totp.token() == token):
                    self.last_t = totp.t()
                    self.save()

                    verified = True
                    break
            else:
                verified = False

        return verified


    def totp_obj(self):
        totp = TOTP(self.bin_key,)
        totp.time = time.time()

        return totp

