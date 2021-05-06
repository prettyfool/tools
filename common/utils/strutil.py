__author__ = 'majunfeng'

import hashlib

def restore_str(like_byte_str):
    """
    there is a string which code like bytes '\xE7\xB2\xBE\xE9\x80\x89\xE8\xA1\xA8\xE6\x83\x85'
    but its type is str, so we need to translate it to a real bytes ,then, we will get a real meaning from bytes to string
    """
    return like_byte_str.encode('raw_unicode_escape').decode('utf-8')


def get_md5(str_code):
    """
    获取字符的md5
    :param str_code: 输入字符串
    :return: 返回md5值
    """
    m = hashlib.md5()
    m.update(str_code.encode('utf-8'))  # hash 时必须进行编码成utf-8
    return m.hexdigest()

if __name__ == '__main__':
    a = '#测试#这是测试#FZXDZ'
    print(get_md5(a).upper())
