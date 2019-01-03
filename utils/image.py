# coding=utf-8
__author__ = 'majunfeng'

import os
from imghdr import what
from tempfile import NamedTemporaryFile

import cv2
from PIL import Image, GifImagePlugin
from requests.api import get


def get_path_url(url):
    res = get(url, stream=True)
    with NamedTemporaryFile('wb+', delete=False) as f:
        f.write(res.content)
        return f.name


def get_first_frame_from_gif(gif_path):
    if not is_gif(gif_path):
        return None
    im = Image.open(gif_path)
    name, ext = os.path.splitext(gif_path)
    frame_path = os.path.join(name, 'frame_{}.png'.format(im.tell())) if ext else name + '.png'
    im.save(frame_path)
    return frame_path


def get_frames_from_gif(gif_path):
    if not is_gif(gif_path):
        return None
    im = GifImagePlugin.GifImageFile(gif_path)
    return im.n_frames


def is_gif(img_path):
    return what(img_path) == 'gif'


def get_path(img_path):
    if not isinstance(img_path, str):
        return None
    if img_path.startswith('http'):
        img_path = get_path_url(img_path)
    if not os.path.isabs(img_path):
        img_path = os.path.abspath(os.path.join(os.curdir, img_path))
    if is_gif(img_path):
        img_path = get_first_frame_from_gif(img_path)
    return img_path


def get_laplacian(img_path):
    im = cv2.imread(img_path)
    img2gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    score = cv2.Laplacian(img2gray, cv2.CV_64F).var()
    return score


class ImageInfo(object):
    def __init__(self, image):
        self.im = Image.open(image)

    def size(self):
        return self.im.size


class ImageCheck(object):
    def __init__(self, image):
        self.im = Image.open(image)

    def verify(self):
        try:
            self.im.load()
        except OSError:
            return False
        else:
            return True


if __name__ == '__main__':
    # img_url = 'http://img04.sogoucdn.com/app/a/200678/8f6bc07c0795440637684f505935a29c.jpg'
    # img_url = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1538070330092&di=5451575b9f1a0d3282207d7a18974b7f&imgtype=0&src=http%3A%2F%2Fb.hiphotos.baidu.com%2Fimage%2Fpic%2Fitem%2Fd52a2834349b033bda7a03101fce36d3d439bd0e.jpg'
    img_url = 'http://img01.sogoucdn.com/app/a/200678/6f4cce8f81bf60b938adf852ebbabea1.jpg'
    img_path = get_path_url(img_url)
    # print(get_frames_from_gif(img_path))
    # print(img_path)
    # im.show()
    # print(get_laplacian(img_path))
