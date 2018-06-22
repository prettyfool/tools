__author__ = 'majunfeng'


def restore_str(like_byte_str):
    """
    there is a string which code like bytes '\xE7\xB2\xBE\xE9\x80\x89\xE8\xA1\xA8\xE6\x83\x85'
    but its type is str, so we need to translate it to a real bytes ,then, we will get a real meaning from bytes to string
    """
    return like_byte_str.encode('raw_unicode_escape').decode('utf-8')


if __name__ == '__main__':
    b = 'GET /pv.gif?uigs_productid=tugeleapp&platform=0&id=ZX1G429PKC&version=4.4.0&channel=test_tugele&aid=1d366f62be7852cc&imei=355470062375429&page=36&action=1&searchSource=4&word=\xE8\x80\x83\xE8\x99\x91\xE8\x80\x83&  \xE7\x9C\x8B\xE7\x9C\x8B&searchHaveResult=1 HTTP/1.0'
    c = '10.129.192.228 [22/Jun/2018:21:20:44 +0800] "GET /pv.gif?uigs_productid=tugeleapp&platform=0&id=ZX1G429PKC&version=4.4.0&channel=test_tugele&aid=1d366f62be7852cc&imei=355470062375429&page=49&action=1&expPackageId=4999&cardId=100&fromPage=79&expPackageName=\xE5\x8D\x96\xE8\x90\x8C\xE5\xB0\x8F\xE7\x86\x8A\xE7\x8C\xAB&cardName=\xE5\xB0\x8F\xE7\xBC\x96\xE6\x8E\xA8\xE8\x8D\x90&firstPage=79&expPackageType=1 HTTP/1.0" -'
    print(restore_str(c))
