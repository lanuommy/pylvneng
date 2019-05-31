import requests
from bs4 import BeautifulSoup
import json
import xlwt

#http://www.lvneng.com/function/selectAllAreaInfo.htm?proId=375
#http://www.lvneng.com/function/selectAllCityInfo.htm?proId=39
book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('list', cell_overwrite_ok=True)

allcity = requests.get('http://www.lvneng.com/function/selectAllProInfo.htm')

count = 0
sheet.write(0, 0, label='省份')
sheet.write(0, 1, label='市县')
sheet.write(0, 2, label='门店地址')

cityinfo = allcity.json()
for i in cityinfo["rows"]:
    getcityID1 = requests.get("http://www.lvneng.com/function/selectAllCityInfo.htm?proId=%s"%(i["cityId"]))
    province = i["cityId"]
    for a in getcityID1.json()["rows"]:
        cityName = a["cityId"]
        allinfo = requests.get("http://www.lvneng.com/point/selectPointInfo.htm?page=1&size=3&pointProviceId=%s&pointCityId=%s&pointStatus=1&pointAreaId:"%(province,cityName))
        for c in allinfo.json()["rows"]:
            count = count + 1
            sheet.write(count, 0, c["pointProviceName"])
            sheet.write(count, 1, c["pointCityName"])
            sheet.write(count, 2, c["pointAddress"])
book.save('/Users/qiao/绿能电动车所有门店信息.xls')

