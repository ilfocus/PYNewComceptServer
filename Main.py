# coding=utf-8

# 导入bmob模块
from bmob import *
import requests
import json

# 新建一个bmob操作对象
b = Bmob("90fbb55de066128374872b20d76a782a",
         "c55b9a86f03531c1998a47dd76480bbb")


def getAllBookInfo():
    data = {
        "method": "recommend",
        "pagesize": "45",
        "pageindex": "0"
    }
    url = "http://www2.uuumeng.com:9090/xingainian/ComicHandle.ashx"
    response = requests.get(url, params=data)
    bookList = response.json()
    return bookList


def getBookInfoWithId(bookId):
    bookList = getAllBookInfo()
    for index in range(len(bookList)):
        bookInfo = bookList[index]
        tempId = bookInfo["BookID"]
        if bookId == tempId:
            return bookInfo

def getBookCatalogWithId(bookId):
    data = {
        "method": "sectionlist",
        "bookid": bookId,
    }
    url = "http://www2.uuumeng.com:9090/xingainian/ComicHandle.ashx"
    response = requests.get(url, params=data)
    bookCatalog = response.json()
    return bookCatalog
def getBookSectionInfoWithSection(section):
    data = {
        "method": "picturelist",
        "sectionid": section,
    }
    url = "http://www2.uuumeng.com:9090/xingainian/ComicHandle.ashx"
    response = requests.get(url, params=data)
    bookSection = response.json()
    print("bookSection",bookSection)
    return bookSection
# print(getBookInfoWithId(0))

# 6 新概念英语第一册美音版
# 13 新概念英语第二册美音版
# 22 新概念英语第三册美音版
# 34 新概念英语第四册美音版
# 5 新概念英语第一册英音版
# 14 新概念英语第二册英音版
# 21 新概念英语第三册英音版
# 33 新概念英语第四册英音版


def uploadBookInfo():
    idMap = {"1": 6, "2": 13, "3": 22, "4": 34,
             "5": 5, "6": 14, "7": 21, "8": 33}

    for key, value in idMap.items() :
        info = getBookInfoWithId(value)
        b.insert(
			'BookInfo',  # 表名
        	BmobUpdater.increment(
            	"count",  # 原子计数key
            	int(key),  # 原子计数值
            	{ # 额外信息
				    "content": json.dumps(info),
				    "user": BmobPointer("_User", "xxx"), # Pointer类型
				    "date": BmobDate(1545098009351) ## Date类型
			    }
        	)
   	 	).jsonData
    print("上传书本信息成功！！！")
    return
def uploadBookCatalog():
    idMap = {"1": 6, "2": 13, "3": 22, "4": 34,
             "5": 5, "6": 14, "7": 21, "8": 33}
    for key, value in idMap.items():
        info = getBookCatalogWithId(value)
        
        for value in info:
            sort = value["Sort"]
            b.insert(
                'BookCatalog' + key,  # 表名
                BmobUpdater.increment(
                    "count",  # 原子计数key
                    sort,  # 原子计数值
                    { # 额外信息
                        "content": json.dumps(info),
                        "user": BmobPointer("_User", "xxx"), # Pointer类型
                        "date": BmobDate(1545098009351) ## Date类型
			        }
                )
            ).jsonData
    print("上传书本目录成功！！！")   
    return
def uplaodBookSectionInfo():
    idMap = {"1": 6, "2": 13, "3": 22, "4": 34,
             "5": 5, "6": 14, "7": 21, "8": 33}
    for key, value in idMap.items():
        info = getBookCatalogWithId(value)
        for value in info:
            SectionID = value["SectionID"]
            BookID = value["BookID"]
            sort = value["Sort"]
            bookSection = getBookSectionInfoWithSection(SectionID)
            b.insert(
                'BookSection' + key,  # 表名
                BmobUpdater.increment(
                    "count",  # 原子计数key
                    sort,  # 原子计数值
                    { # 额外信息
                        "content": json.dumps(bookSection),
                        "BookID" : BookID
			        }
                )
            ).jsonData
    print("上传书本信息成功！！！")   
    return
def main():
    # uploadBookInfo()
    # uploadBookCatalog()
    uplaodBookSectionInfo()
    return
main()