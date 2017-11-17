from re import findall
import os
import hashlib
import requests
import json


def getApkUrl():
    """get all lastscuccessful release build of tugele"""
    # url = 'http://10.134.242.187:8080/job/SGTugele/lastSuccessfulBuild/artifact/bin/'
    url = 'http://10.134.242.187:8080/job/ASTugele/lastSuccessfulBuild/artifact/app/build/outputs/apk/'
    res = requests.get(url).content
    filelist = findall('(SGTugele[a-zA-Z0-9_.]+)">', res)
    print res
    urls = [os.path.join(url, filename) for filename in filelist]
    if len(urls) == 1:
        return urls[0]
    else:
        return urls[21]


def parseurl(url):
    name = os.path.splitext(os.path.basename(url))[0]
    tempdict = {}
    tempdict["version"] = name.split('_')[1][1:]
    tempdict["buildcode"] = name.split('_')[3]
    tempdict["url"] = url
    tempdict["needUpdate"] = 0
    tempdict["updateLog"] = "version : %(version)s buildcode : %(buildcode)s" % (tempdict)
    return tempdict


def getContent(url):
    return requests.get(url).content


def getMd5(content):
    md5 = hashlib.md5()
    md5.update(content)
    strMd5 = md5.hexdigest()
    return strMd5


def getApkMd5(url):
    content = getContent(url)
    return getMd5(content)


def getJsonStr():
    url = getApkUrl()
    finaldict = parseurl(url)
    finaldict["md5"] = getApkMd5(url)
    return json.dumps(finaldict)


def getCheckFile(strJson):
    filepath = r"E:\TestData\fiddler_tugele\version.txt"
    print "Get file : %s" % filepath
    with open(filepath, "wb") as f:
        f.write(strJson)


def getApkFile():
    url = getApkUrl()
    dirpath = r"E:\package\PKG_tugele"
    apkname = os.path.basename(url)
    apkfile = os.path.join(dirpath, apkname)
    content = getContent(url)
    with open(apkfile, "wb") as fi:
        fi.write(content)
    print 'Download apk : %s' % apkfile


def main():
    strJson = getJsonStr()
    getCheckFile(strJson)
    getApkFile()


if __name__ == '__main__':
    main()
