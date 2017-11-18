# coding:utf-8
import re
import requests
import os

try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET
import shutil
from logUtil import logger

result = {}


# 1.下载所有的渠道包到指定目录

def tugeleLinks():
    """
    @des 获取所有的渠道包下载连接
    @urls 返回所有下载链接列表
    """
    logger.info('get download links...')
    url = 'http://10.134.242.187:8080/job/SGTugele/lastSuccessfulBuild/artifact/bin/'
    res = requests.get(url).content
    filelist = re.findall('(SGTugele[a-zA-Z0-9_.]+)">', res)
    urls = [os.path.join(url, filename) for filename in filelist]
    return urls


def downAPK(url, out='./'):
    """
	@des 下载文件
	@url 下载链接
	"""
    try:
        r = requests.get(url, stream=True, verify=False)
    except requests.exceptions.HTTPError, e:
        print '%s is Error\n%s' % (url, e)
    else:
        name = os.path.basename(url)
        file_name = os.path.join(out, name)
        CHUNK_SIZE = 16 * 1024
        with open(file_name, 'wb') as f:
            logger.debug('success download %s' % name)
            for chunk in r.iter_content(CHUNK_SIZE):
                f.write(chunk)


# 2.解析安装包获取Manifest文件中的渠道号和pushTag

def getManifest(path):
    """
	@des 解apk包
	"""
    cmd = 'java -jar apktool.jar d %s > nul' % path
    logger.info('parsing package.....')
    logger.info(os.path.basename(path))
    os.system(cmd)


def getChannel(xml):
    """
	@des 解析Manifest.xml获取channelID,pushTag
	@param xml xml文件的路径
	@return [channelID,pushTag]
	"""
    res = []
    tree = ET.parse(xml)
    application = tree.getroot().find('application')
    for meta in application.findall('meta-data'):
        if meta.get('android:name') == "SGTUGELE_CHANNEL_ID":
            res.append(meta.get('android:value'))
        if meta.get('android:name') == "SGTUGELE_PUSH_TAG":
            res.append(meta.get('android:value'))
    return res


def getTemp():
    dirs = os.listdir('./')
    for i in dirs:
        if i.startswith('SG') and os.path.isdir(i):
            return i


# 3.验证渠道号和pushTag
def verify(path):
    """
	@des 验证渠道号和pushtag
	@path 安装包路径
	"""
    getManifest(path)
    temp = getTemp()
    channel, pushtag = getChannel(os.path.join(temp, 'AndroidManifest.xml'))
    if pushtag == 'online' and channel in path:
        result[channel] = 'pass'
    else:
        result[channel] = 'fail'
    logger.info('Verifying ...')


# 4.清理文件

def delfile(src):
    """
	@desc 删除非空目录src
	@src 非空目录全路径
	"""
    shutil.rmtree(src)


def clear():
    """
	@desc 清理目录
	"""
    temp = getTemp()
    logger.info('clear directory ')
    delfile(temp)


# 5.生成报告
def report():
    """
	@desc 把测试通过的渠道号写入result.txt
	"""
    logger.info('get report file...')
    with open('result.txt', 'w') as f:
        for item in result:
            f.write(item)
            f.write('\n')


if __name__ == '__main__':
    # if not os.path.exists('package'):
    #     logger.info('package is not exist ,creating it...')
    #     os.mkdir('package')

    package_path = r'D:\mobile'  # 渠道包的目录地址
    apklist = os.listdir(package_path)
    if not len(apklist):
        logger.error('no apk fils in %s' % package_path)
        exit()
    for apk in apklist:
        path = os.path.join(package_path, apk)
        verify(path)
        clear()
    report()
