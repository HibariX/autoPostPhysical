__version__ = 0.3

import requests
import re
import json
import argparse
import datetime


# get arguments
parser = argparse.ArgumentParser(description='自动填写健康表')
parser.add_argument('--username', '-u', help='用户名', required=True)
parser.add_argument('--password', '-p', help='密码', required=True)
parser.add_argument('--permanentaddress', '-a', help='常住地址', required=True)
parser.add_argument('--todayaddress', '-t', help='今日地址',
                    default='广东省珠海市金湾区吉林大学珠海学院')
args = parser.parse_args()
username = args.username        # 用户名
password = args.password  		# 密码
jtdz = args.permanentaddress    # 常住地址
xjzdz = args.todayaddress       # 当天居住地址

# get date & time
today_date = datetime.datetime.now().strftime('%Y-%m-%d')
cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

session = requests.Session()

# login(post)
# -- get html
url = "https://authserver.jluzh.com/cas/login?service=https%3A%2F%2Fwork.jluzh.com%2Fdefault%2Fwork%2Fjl" \
      "zh%2Fjkxxtb%2Fjkxxcj.jsp%3Fappload%3D0%26f%3Dapp"
response = session.get(url=url)
html = response.text
# -- get execution para
execution_re = re.findall('name="execution" value=".*/>', html)
if len(execution_re) > 0:
    execution = execution_re[0].replace(
        'name="execution" value="', '').replace('" />', '')
    print(f'execution:{execution}')
else:
    print('execution para is none')
    exit()
data = {
    'username': username,
    'password': password,
    'execution': execution,
    '_eventId': "submit",
    'loginType': 1,
    'submit': "登  录"
}

response = session.post(url=url, data=data)
print(f"login status code: {response.status_code}")


# query base info
url_temp = "https://work.jluzh.com/default/work/jlzh/jkxxtb/com.sudytech.portalone.base.db.queryBySqlWithoutPagecond.biz.ext"
data = {
    'params': {
        'empcode': username
    },
    "querySqlId": "com.sudytech.work.jlzh.jkxxtb.jkxxcj.queryNear",

}
session.headers['content-type'] = 'application/json'        # Request Payload

response = session.post(url=url_temp, data=json.dumps(data))
query_json = response.json()
list_json = query_json.get("list", [{}])[0]
print("list_json", list_json)


# submit form(post)
form_data = {
	'entity':{
		'bjmc': list_json['BJMC'],
		'bt': f"{today_date} {list_json['SQRMC']} 健康卡填报",
		'bz': list_json['BZ'],
		'cn': ["本人承诺登记后、到校前不再前往其他地区"],
		'fdygh': list_json['FDYGH'],
		'fdymc': list_json['FDYMC'],
		'gh': list_json['GH'],
		'grjkzk': list_json['GRJKZK'],
		'id': list_json['ID'],
		'jkqk': list_json['JKQK'],
		'jqqx': list_json['JQQX'],
		'jrtw': list_json['JRTW'],
		'jtdz': jtdz,
		'lxdh': list_json['LXDH'],
		'nj': list_json['NJ'],
		'qsjkzk': list_json['QSJKZK'],
		'rysf': "2",
		'sfjchbjry': "否",
		'sfjwhy': "否",
		'sfjwhygjdq': "",
		'sfqwhb': "否",
		'sqbmid': list_json['SQBMID'],
		'sqbmmc': list_json['SQBMMC'],
		'sqrid': list_json['SQRID'],
		'sqrmc': list_json['SQRMC'],
		'ssh': list_json['SSH'],
		'tbrq': today_date,
		'tjsj': cur_time,
		'xb': "1",
		'xjzdz': xjzdz,
		'xrywz': "2",
		'zymc': list_json['ZYMC'],
		'__type': "sdo:com.sudytech.work.jlzh.jkxxtb.jkxxcj.TJlzhJkxxtb",
		'_ext': "{}"
	}
}
url = "https://work.jluzh.com/default/work/jlzh/jkxxtb/com.sudytech.portalone.base.db.saveOrUpdate.biz.ext"

response = session.post(url=url, data=json.dumps(form_data))
print(response.text)
result = response.json()["result"]
if result == "1":
    print('提交成功')
else:
    print("提交失败")