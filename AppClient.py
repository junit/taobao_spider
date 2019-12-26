# !/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import requests
from urllib.parse import quote_plus
import time
import random
import string

appKey = "21646297"
ttid = '1568707896704@taobao_android_9.1.0'
app_ver = "9.1.0"
ua = "MTOPSDK%2F3.1.1.7+%28Android%3B5.1.1"
Cookie = ""
utdid = "iGuuZCilkcOBojXEIkDESMPP"
lat = ""
lng = ""


def random_str(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for x in range(length))


def call_gw_api(sign_server, api, v, data, use_cookie=False, uid='', sid='', features='27', method='GET'):
    timestamp = time.time()
    t = int(timestamp)
    deviceId = random_str(44)
    pageId = "http://h5.m.taobao.com/taolive/video.html"
    pageName = "com.ali.user.mobile.login.ui.UserLoginActivity"
    pre_sign_data = {
        "uid": uid,
        "ttid": ttid,
        "data": quote_plus(data),
        "lng": lng,
        "utdid": utdid,
        "api": api,
        "lat": lat,
        "deviceId": deviceId,
        "sid": sid,
        "x-features": features,
        "v": v,
        "t": str(t),
        "pageName": pageName,
        "pageId": pageId
    }
    sign_dic = get_sign_dic(sign_server, pre_sign_data)

    body = "data=" + quote_plus(data)
    req_url = "https://guide-acs.m.taobao.com/gw/{0}/{1}/".format(api, v)

    headers = {
        "x-appkey": appKey,
        "x-devid": deviceId,
        "x-ttid": quote_plus(ttid),
        "x-sign": quote_plus(sign_dic['result']['x-sign']),
        "x-mini-wua": quote_plus(sign_dic['result']['x-mini-wua']),
        "x-sgext": sign_dic['result']['x-sgext'],
        "x-t": str(t),
        "x-location": quote_plus("{0},{1}".format(lng, lat)),
        "x-app-ver": app_ver,
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        "x-pv": "6.3",
        "x-features": features,
        "x-app-conf-v": str(19),
        "x-utdid": utdid,
        "User-Agent": ua,
    }

    if uid != "":
        headers["x-uid"] = uid
        headers["x-sid"] = sid
    if use_cookie:
        headers["Cookie"] = Cookie

    print("开始请求:" + api)
    print("请求淘宝Http头:")
    for key in headers.keys():
        print(key + ":" + headers[key])

    if method == 'GET':
        print("请求淘宝Http方式: GET")
        req_url = "https://trade-acs.m.taobao.com/gw/{0}/{1}/?{2}".format(api, v, body)
        print("请求淘宝url:" + req_url)
        sign_dic = requests.get(req_url, headers=headers, verify=True)

    else:
        print("请求淘宝Http方式: POST")
        print("请求淘宝url:" + req_url)
        print("请求淘宝参数:" + body)
        sign_dic = requests.post(req_url, data=body, headers=headers, verify=True)

    if sign_dic.status_code == requests.codes.ok:
        print("淘宝返回:" + sign_dic.text)
        print("\n")


def get_sign_dic(sign_server, payload):
    headers = {
        "content-type": "application/json;charset=utf-8"
    }
    print("待签名参数:" + json.dumps(payload))
    res = requests.post(sign_server, data=json.dumps(payload), headers=headers)
    res_content = res.content
    print("签名返回:" + str(res_content))
    sign_dic = {}
    if res.status_code == requests.codes.ok:
        sign_dic = json.loads(res_content)
    return sign_dic


def get_live_detail(sign_server, live_id):
    data = "{\"extendJson\":\"{\\\"guardAnchorSwitch\\\":true,\\\"version\\\":\\\"201903\\\"}\",\"ignoreH265\":\"false\",\"live_id\":\"" + live_id + "\"}"
    v = "4.0"
    api = "mtop.mediaplatform.live.livedetail"
    call_gw_api(sign_server, api, v, data)


def w_search(sign_server, q):
    t = str(int(time.time()))
    q = quote_plus(q)
    data = "{\"LBS\":\"{\\\"SG_TMCS_1H_DS\\\":\\\"{\\\\\\\"stores\\\\\\\":[]}\\\",\\\"SG_TMCS_FRESH_MARKET\\\":\\\"{\\\\\\\"stores\\\\\\\":[]}\\\",\\\"TB\\\":\\\"{\\\\\\\"stores\\\\\\\":[{\\\\\\\"code\\\\\\\":\\\\\\\"156775275\\\\\\\",\\\\\\\"type\\\\\\\":\\\\\\\"4\\\\\\\"}]}\\\",\\\"TMALL_MARKET_B2C\\\":\\\"{\\\\\\\"stores\\\\\\\":[]}\\\",\\\"TMALL_MARKET_O2O\\\":\\\"{\\\\\\\"stores\\\\\\\":[{\\\\\\\"code\\\\\\\":\\\\\\\"236829063\\\\\\\",\\\\\\\"bizType\\\\\\\":\\\\\\\"DELIVERY_TIME_HALF_DAY\\\\\\\",\\\\\\\"type\\\\\\\":\\\\\\\"CHOOSE_ADDR\\\\\\\"}]}\\\"}\",\"URL_REFERER_ORIGIN\":\"https://s.m.taobao.com/h5entry\",\"ad_type\":\"1.0\",\"apptimestamp\":\"" + t + "\",\"areaCode\":\"CN\",\"brand\":\"\",\"cityCode\":\"\",\"countryNum\":\"156\",\"device\":\"\",\"editionCode\":\"CN\",\"filterEmpty\":\"true\",\"filterUnused\":\"true\",\"from\":\"input\",\"homePageVersion\":\"v6\",\"imei\":\"\",\"imsi\":\"\",\"info\":\"wifi\",\"isEnterSrpSearch\":\"true\",\"itemfields\":\"commentCount,newDsr\",\"jarvisDisable\":\"true\",\"latitude\":\"" + lat + "\",\"layeredSrp\":\"true\",\"longitude\":\"" + lng + "\",\"n\":\"10\",\"needTabs\":\"true\",\"network\":\"wifi\",\"new_shopstar\":\"true\",\"page\":\"1\",\"q\":\"" + q + "\",\"rainbow\":\"13406,11837,13724,12995,13977,13321,14070\",\"referrer\":\"http://s.m.taobao.com/search.htm?spm=a2141.7631694.0.0&q=" + quote_plus(
            q) + "\",\"schemaType\":\"auction\",\"searchDoorFrom\":\"srp\",\"searchFramework\":\"true\",\"search_action\":\"initiative\",\"search_wap_mall\":\"false\",\"setting_on\":\"imgBanners,userdoc,tbcode,pricerange,localshop,smartTips,firstCat,dropbox,realsale,insertTexts,tabs\",\"showspu\":\"true\",\"sputips\":\"on\",\"style\":\"list\",\"sversion\":\"8.0\",\"taoxianda\":\"true\",\"ttid\":\"" + ttid + "\",\"utd_id\":\"" + utdid + "\",\"vm\":\"nw\"}"
    v = "1.0"
    api = "mtop.taobao.wsearch.appsearch"
    call_gw_api(sign_server, api, v, data, True)


if __name__ == '__main__':
    sign_server = "http://192.168.3.5:6778/xsign"

    live_id = '248743342811'
    get_live_detail(sign_server, live_id)

    q = '牛仔裤'
    w_search(sign_server, q)
