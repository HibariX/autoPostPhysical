__version__ = 0.1

import requests
import re
import json

session = requests.Session()

# user setting
username = ""           # 用户名
password = ""           # 密码
jtdz = ""               # 常住地址
xjzdz = ""              # 当天居住地址
form_data = {"entity": {}}
# get html
url = "https://authserver.jluzh.com/cas/login?service=https%3A%2F%2Fwork.jluzh.com%2Fdefault%2Fwork%2Fjlzh%2Fjkxxtb%2Fjkxxcj.jsp%3Fappload%3D0%26f%3Dapp"
response = session.get(url=url)
html = response.text

# get execution para
execution_re = re.findall('name="execution" value=".*/>', html)
if len(execution_re) > 0:
	execution = execution_re[0].replace('name="execution" value="', '').replace('" />', '')
	print(f'execution:{execution}')
else:
	print('execution para is none')
	exit()

# init data
data = {
	'username': username,
	'password': password,
	'execution': execution,
	'_eventId': "submit",
	'loginType': 1,
	'submit': "登  录"
}

# login(post)
response = session.post(url=url, data=data)
print(f"login status code: {response.status_code}")

# test is login success ?
url_temp = "https://work.jluzh.com/default/work/jlzh/jkxxtb/com.sudytech.portalone.base.db.queryBySqlWithoutPagecond.biz.ext"
data = {
	'params': {
		'empcode': username
	},
	"querySqlId": "com.sudytech.work.jlzh.jkxxtb.jkxxcj.queryToday",
	
}
session.headers['content-type'] = 'application/json'        # Request Payload
response = session.post(url=url_temp, data=json.dumps(data))
query_json = response.json()
print("query", response.text)
form_data['entity'] = query_json

# submit form(post)
form_data['entity']["__type"] = "sdo:com.sudytech.work.jlzh.jkxxtb.jkxxcj.TJlzhJkxxtb"
form_data['entity']["_ext"] = "{}"
form_data['entity']['jtdz'] = jtdz
form_data['entity']['xjzdz'] = xjzdz
url = "https://work.jluzh.com/default/work/jlzh/jkxxtb/com.sudytech.portalone.base.db.saveOrUpdate.biz.ext"

response = session.post(url=url, data=json.dumps(form_data))
print(response.text)

result = response.json()["result"]
if result == "1":
	print('提交成功')
else:
	print("提交失败")