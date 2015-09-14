# Production specific settings
import re, os

db_url = 'postgres://qqktnfzrapcmcd:91OFOYWsc1MtT50VNB3gId7ka-@ec2-46-137-159-123.eu-west-1.compute.amazonaws.com:5432/d11pcgnfhar7ec'
regex = r'postgres\:\/\/(\w+)\:([\w\-]+)@([\w\-\.]+)\:(\d+)\/(\w+)'
pattern = re.compile(regex)
matches = pattern.match(db_url)

# Database configuration
DATABASES['default']['USER'], DATABASES['default']['PASSWORD'], DATABASES['default']['HOST'], DATABASES['default']['PORT'], DATABASES['default']['NAME'] = matches.groups()
