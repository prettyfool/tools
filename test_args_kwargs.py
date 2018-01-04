# coding=utf-8
__author__ = 'majunfeng'


def test_kwargs(**kwargs):
    for k, v in kwargs.items():
        print('{}:{}'.format(k, v))


def test_args(*args):
    for i in args:
        print(i)


dd = {
    'a': 'abc',
    'b': 'bbc'
}

aa = ['a', 'b', 'c']

test_kwargs(**dd)
test_args(*aa)
