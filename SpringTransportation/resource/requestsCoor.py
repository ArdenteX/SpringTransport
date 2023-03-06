import requests
import json
from lxml import etree
import my_fake_useragent


def find_coordination(city):
  HEADERS = {
    'user_agent': my_fake_useragent.UserAgent().random(),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Cache-Control': 'max-age=0',
  }

  k_v = {'keyword': city, 'txtflag': 0}

  res = requests.post('http://www.jsons.cn/lngcode/', data=k_v, headers=HEADERS)
  data = etree.HTML(res.text)
  xpath = "//table[@class='table table-bordered table-hover']//tr[1]/td[3]/text()"

  return data.xpath(xpath)[0].strip()





