#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by vellhe 2020/10/21
#pip安装下下面这些包例如 pip install Flask
from flask_cors import *
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask import request
import re
import requests
import json

headers = {
    "User-Agent":"Mozilla/5.0 (Linux; Android 5.1.1; vmos Build/LMY48G; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 MicroMessenger/7.0.12.1620(0x27000C34) Process/appbrand2 NetType/WIFI Language/zh_CN ABI/arm32",
}

app = Flask(__name__)
api = Api(app)
CORS(app, supports_credentials=True)

parser = reqparse.RequestParser()
parser.add_argument('task')


def parseUrl(string):
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式
    url = re.findall(pattern, string)
    return url

class Todo(Resource):

    # 获取抖音真实地址
    def getUrl(string):
        url_arr = []
        for i in parseUrl(string):
           url_arr.append(parseOneUrl(str(i).strip()))        
        return url_arr;

    # 解析单个链接
    @app.route('/douyin/', methods=['post'])
    def parseOneUrl():
        try:
            # 提取出来的磁力链接数组
            URL = parseUrl(request.form.get("url"))
            error = None
            resultMap = {}
            resultArr = []
            for u in URL:
                res = requests.head(u)
                local = res.headers['location'];
                start = local.index("video") + 6
                end = local.index("/?region")
                ite = local[start:end]
                url = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=" + str(ite)
                json = requests.get(url).json()
                parUrl = json['item_list'][0]['video']['play_addr']['url_list'][0]
                Url = str(parUrl).replace("playwm", "play")
                response = requests.head(Url, headers=headers)
                resultArr.append(response.headers['location'])
                resultMap['code'] = "200"
                resultMap['data'] = resultArr
            return resultMap
        except Exception:
            map = {}
            map["code"] = "500"
            map["data"] = "出错了哦，亲~"
            return map

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
