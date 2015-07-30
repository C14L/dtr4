
import re
from django.utils.text import slugify as dj_slugify

def slugify(s):
    return re.sub('[^A-Za-z0-9]+', '-', dj_slugify(s))

def slugify_a_z(s):
    # Converts none ascii alpha into ascii and then removes anything else.
    return re.sub('[^a-z]+', '', dj_slugify(s))

# ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits
# remove u/U and e/E to avoid several swear words "c*nt", "f*ck", "s*ck"
# remove I/l and 0/O because ambiguous.
# Then mix the rest up a bit.
ALPHABET = '1dmcFJT3h4DxfgyBSZn6t7a8zAVWXjkY92bNPQsGHo5KLvwipqrCMR'
ALPHABET_REVERSE = dict((c, i) for (i, c) in enumerate(ALPHABET))
BASE = len(ALPHABET)
SIGN_CHARACTER = '-'

def num_encode(n):
    if n is None:
        raise ValueError('Called num_encode() with None value.')
    if n < 0:
        return SIGN_CHARACTER + num_encode(-n)
    s = []
    while True:
        n, r = divmod(n, BASE)
        s.append(ALPHABET[r])
        if n == 0: break
    return ''.join(reversed(s))

def num_decode(s):
    if s[0] == SIGN_CHARACTER:
        return -num_decode(s[1:])
    n = 0
    for c in s:
        n = n * BASE + ALPHABET_REVERSE[c]
    return n

def get_client_ip(request):
    """
    Returns the public IP address of a request client, or None it no IP 
    address could be found.

    From: http://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', None)
    if x_forwarded_for:
        # The right-most IP is the proxy's public address.
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        # Not a proxy, get the remote address.
        ip = request.META.get('REMOTE_ADDR', None)
    return ip

def get_client_ip_as_int(request):
    return ip4_to_int(get_client_ip(request))

def ip4_to_int(s):
  "Convert dotted IPv4 address to integer."
  return reduce(lambda a,b: a<<8 | b, map(int, s.split(".")))
 
def int_to_ip4(ip):
  "Convert 32-bit integer to dotted IPv4 address."
  return ".".join(map(lambda n: str(ip>>n & 0xFF), [24,16,8,0]))
