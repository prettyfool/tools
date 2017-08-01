# coding:utf-8
import re
import requests
from lxml import etree
import os
import shutil
import logger

logger = logger.logger
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

def downAPK(url,out='./'):
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
			logger.debug('success download %s'%name)
			for chunk in r.iter_content(CHUNK_SIZE):
				f.write(chunk)


# 2.解析安装包获取Manifest文件中的渠道号和pushTag

def getManifest(path):
	"""
	@des 解apk包到temp目录
	"""
	cmd = 'java -jar apktool.jar d %s -o temp > nul'%path
	logger.info('parsing package...')
	logger.info(os.path.basename(path))
	os.system(cmd)

def getChannel(xml):
	"""
	@des 解析Manifest.xml获取channelID,pushTag
	@return [channelID,pushTag]
	"""
	info = {}
	tree = etree.parse(xml)
	meta = tree.xpath('//meta-data')
	return [me.values()[1] for me in meta][0:2]


# 3.验证渠道号和pushTag
def verify(path):
	"""
	@des 验证渠道号和pushtag
	@path 安装包路径
	"""
	getManifest(path)
	channel,pushtag = getChannel('temp\AndroidManifest.xml')
	if pushtag =='online' and channel in path:
		result[channel] = 'pass'
	else:
		result[channel] = 'fail'
	logger.info('Verifying ...')


# 4.清理文件

def delfile(src):
	shutil.rmtree(src)

#abandon
def delfile1(src):
	if os.path.isfile(src):
		os.remove(src)
	if os.path.isdir(src):
		fi = os.listdir(src)
		if len(fi):
			for i in fi:
				p = os.path.join(src,i)
				delfile(p)
		else:
			os.rmdir(src)

def clear():
	src = r'.\temp'
	logger.info('clear directory temp...')
	delfile(src)

# 5.生成报告
def report():
	logger.info('get report file...')
	with open('result.txt','w') as f:
		for item in result:
			f.write(item)
			f.write('\n')


if __name__ == '__main__':
	#下载所有安装包
	if not os.path.exists('package'):
		logger.info('package is not exist ,creating it...')
		os.mkdir('package')
	apklist = os.listdir('package')
	if not len(apklist):
		links = tugeleLinks()
		logger.info('downloading ...')
		for url in links:
			downAPK(url,out='package')
		apklist = os.listdir('package')

	for apk in apklist:
		path = os.path.join(os.curdir,'package',apk)
		verify(path)
		clear()
	report()

