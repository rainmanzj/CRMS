import hashlib


def gen_md5(value):
    res = hashlib.md5(b'123asdfajweif')
    res.update(value.encode('utf-8'))
    return res.hexdigest()
