from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import chardet, time, random
import re, os
import pickle

'''
程序思路，找到任何关大学生、兼职的贴吧，自动发帖。
'''
# 创建chrome浏览器对象
browser = webdriver.Chrome()

# 贴吧及帖子信息（帖子标题已经内容需随机选取）
tieba_name = '浙江大学'
title = '测试'
text = '出售自己的小米笔记本，需要的私聊'

flag = True
# cookies存放地址
path = 'tieba.p'

# 判断置顶帖中字符
s = ['二手','广告','交易','兼职','集中','信息']

# 页面find
url = 'https://tieba.baidu.com/'
search_xpath = '//input[@id="wd1"]'
focus_id = 'j_head_focus_btn'
head_id = 'forum-card-head'
my_id = 'my_tieba_mod'
fatie_xpath = '//li[@class="tbui_aside_fbar_button tbui_fbar_post"]/a'
title_xpath = '//div[@class="j_title_wrap"]/input'
editor_xpath = '//div[@class="edui-editor-middle"]'
# 普通帖发表
fabiao_xpath = '//button[@class="btn_default btn_middle j_submit poster_submit"]'
top_xpath = '//i[@class="icon-top"]/following-sibling::a'

# 回复帖发表
fabiaoBack_xpath = '//a[@class="ui_btn ui_btn_m j_submit poster_submit"]'
# 签到
sign_xpath = '//div[@id="signstar_wrapper"]/a'
# 测试，获取首页上关注的贴吧
u_f_w = '//div[@id="likeforumwraper"]//a'
'''
Cookie: TIEBA_USERTYPE=c57bab2ce9e9346202f2cbb1; BAIDUID=0895DDFDFA4491EDC0660C08CCC29151:FG=1; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1555292867; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1555292867; BIDUPSID=0895DDFDFA4491EDC0660C08CCC29151; PSTM=1555292874; BDRCVFR[abe9uUBlp-C]=mk3SLVN4HKm; delPer=0; H_PS_PSSID=1435_21100_28774_28723_28558_28832_28585_28604_28626_28606; BDUSS=U80ME9NYmJSQ0QyRGRHZW8tTHMtOVlPdVpjaGVoUHNlcFNzQ3kxVG43VVZjTnRjRVFBQUFBJCQAAAAAAAAAAAEAAAA7U61hVEVB0KF2AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABXjs1wV47Nca; STOKEN=489c5b69434d345ac4b18cdb1d80760109718205aa51373a7cc9f4cafc3e9959; TIEBAUID=08df9b3bf645c84d5df67f4a
[{'domain': '.tieba.baidu.com', 'expiry': 1609430397.207513, 'httpOnly': False, 'name': 'TIEBAUID', 'path': '/', 'secure': False, 'value': '08df9b3bf645c84d5df67f4a'}, {'domain': '.tieba.baidu.com', 'expiry': 1609430397.181403, 'httpOnly': False, 'name': 'TIEBA_USERTYPE', 'path': '/', 'secure': False, 'value': 'edaa8f291df20c6381e780bb'}, {'domain': '.baidu.com', 'expiry': 1586830328.18147, 'httpOnly': False, 'name': 'BAIDUID', 'path': '/', 'secure': False, 'value': '64BC44CF0D6719730729F9C2A6465C72:FG=1'}, {'domain': '.tieba.baidu.com', 'expiry': 1586830384, 'httpOnly': False, 'name': 'Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948', 'path': '/', 'secure': False, 'value': '1555294331'}, {'domain': '.baidu.com', 'expiry': 1814494380.547409, 'httpOnly': True, 'name': 'BDUSS', 'path': '/', 'secure': False, 'value': 'I5Y3ByZEVoUDVuUmdGVk1COW44Ti1KSHBSdHd5OFNTNnVhS3Fpb2ZScXZkZHRjRVFBQUFBJCQAAAAAAAAAAAEAAAA7U61hVEVB0KF2AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAK~os1yv6LNcY3'}, {'domain': '.tieba.baidu.com', 'expiry': 1557886382.468427, 'httpOnly': True, 'name': 'STOKEN', 'path': '/', 'secure': False, 'value': '4f1931b711a21097f67b6ef74ba6f480f652c978f2256b1c30536fc960ca8ef0'}, {'domain': '.tieba.baidu.com', 'httpOnly': False, 'name': 'Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948', 'path': '/', 'secure': False, 'value': '1555294385'}]
'''
# 可用By.XPATH,"//*[@id='nr']/option[1]"
# wait.until(EC.presence_of_element_located((By.ID,'com_userbar')))

# 获得登陆cookies并储存在本地
def getTiebaCookies():
	browser.get(url)
	# browser.maximize_window()
	wait = WebDriverWait(browser, 60)
	print("请手动登陆")

	# 可用By.XPATH,"//*[@id='nr']/option[1]"
	wait.until(EC.presence_of_element_located((By.ID, my_id)))

	tbcookies = browser.get_cookies()
	browser.quit()

	# cookies = {}
	# for item in tbcookies:
	# 	cookies[item['name']] = item['value']
	with open(path, 'wb') as f:
		pickle.dump(tbcookies, f)
		f.close()
	return tbcookies

def readTiebaCookies():
	if os.path.exists(path):
		tbcookies = pickle.load(open(path, 'rb'))
	else:
		tbcookies = getTiebaCookies()
	return tbcookies

tbcookies = readTiebaCookies()
browser.get(url)
# print(browser.get_cookies())

for cookies in tbcookies:
	browser.add_cookie(cookies)
time.sleep(2)

try:
	browser.refresh()
	wait = WebDriverWait(browser, 5)

	# print(browser.get_cookies())

	wait.until(EC.presence_of_element_located((By.ID, my_id)))
	print("登陆成功")
except Exception as e:
	print(e)
	print("登陆失败")

# 找多个元素一定要用find_elements
# t = browser.find_elements_by_xpath(u_f_w)
# for x in t:
# 	print(x.get_attribute('title'))

# 开始搜索贴吧并发帖，封装成方法

'''发帖分三种：
1.在置顶广告集中帖发回复帖

2.普通发帖（普通贴自动顶帖）

3.回复热门帖（可选）

'''

# 判断是否为广告信息集中帖
def veryfy(tops):
	for top in tops:
		linkText = top.get_attribute("title")
		for x in s:
			if (x in linkText):
				return True, top
				break
	return False, '置顶帖无广告集中贴'

# 判断节点是否存在
def is_element_exist(xpath):
	try:
		time.sleep(0.2)
		browser.find_element_by_xpath(xpath)
		return True
	except:
		return False

# 普通发帖方法
def normal_post(title, text):
	try:
		# 直接发帖步骤
		# 点击发帖
		browser.find_element_by_xpath(fatie_xpath).click()

		# 输入标题
		time.sleep(0.1)
		title_input = browser.find_element_by_xpath(title_xpath)
		# title.click()
		title_input.send_keys(title)

		# 输入内容(由于找不到textarea，于是使用js填入帖子内容)
		time.sleep(0.2)
		js = '$("div#ueditor_replace p").html("%s")' % (text, )
		# js = "document.getElementsByTagName('p')[12].innerText='%s'" % (text, )
		browser.execute_script(js)

		# 发表
		time.sleep(0.1)

		browser.find_element_by_xpath(fabiao_xpath).click()
		time.sleep(2)
		print("%s贴吧普通发帖成功" % (tieba_name, ))
	except Exception as e:
		print(e)
		print("%s贴吧普通发帖失败" % (tieba_name, ))

# 置顶帖回复
def back_post(top, text):
	try:
		top.click()
		# 需要切换窗口句柄，不然定位不到新的窗口上的元素
		# 当前窗口句柄
		top_handle = browser.current_window_handle
		# 所有句柄集合
		handles = browser.window_handles
		# 得到新窗口句柄
		for handle in handles:
			if handle !=top_handle:
				back_handle = handle
		# 切换句柄
		browser.switch_to.window(back_handle)
		time.sleep(2)
		js = '$("div#ueditor_replace p").html("%s")' % (text, )
		browser.execute_script(js)
		browser.find_element_by_xpath(fabiaoBack_xpath).click()
		time.sleep(2)
		print("%s吧置顶帖发帖成功" % (tieba_name, ))
		browser.close()
		browser.switch_to.window(top_handle)
		time.sleep(2)
	except Exception as e:
		print(e)
		print("%s吧置顶帖发帖失败" % (tieba_name, ))

# 发帖方法，参数为贴吧名，帖标题，贴文字
def tieba_post(tieba_name, title, text):
	search_input = browser.find_element_by_xpath(search_xpath)
	# print(browser.get_cookies())
	search_input.clear()
	search_input.send_keys(tieba_name)
	search_input.send_keys(Keys.ENTER)
	time.sleep(1)
	global flag
	if (flag):
		for cookies in tbcookies:
			browser.add_cookie(cookies)
		time.sleep(2)
		browser.refresh()
		flag = False
	# 出现broswer新开的网页不带cookies情况，即broswer对象为开的第一个网页

	# 如果没有直接跳转到贴吧主页，则说明该贴吧名不存在
	try:
		wait = WebDriverWait(browser, 3)
		wait.until(EC.presence_of_element_located((By.ID, head_id)))
	except Exception as e:
		print(e)
		print('%s吧不存在！' % (tieba_name, ))
		return False
	# print(browser.get_cookies())

	# 获取到关注按钮
	focus = browser.find_element_by_id(focus_id)

	# 判断是否已经关注,若没关注点击关注，关注则直接发帖
	deter = focus.get_attribute('class')
	if (deter != 'focus_btn cancel_focus'):
		focus.click()
		time.sleep(1)
		print('%s吧关注成功' % (tieba_name, ))
		# 关闭弹出窗口
		browser.find_element_by_xpath('//a[@class = "dialogJclose"]').click()
	time.sleep(0.2)

	# 自动签到
	sign = browser.find_element_by_xpath(sign_xpath)
	if sign.get_attribute("class") != "j_signbtn signstar_signed":
		# 单击一次不能成功签到，双击事件也不行，只能单击后再点一次，签到成功
		sign.click()
		time.sleep(0.1)
		sign.click()
		time.sleep(1)
		sign = browser.find_element_by_xpath(sign_xpath)
		if sign.get_attribute("class") == "j_signbtn signstar_signed":
			print('%s吧签到成功' % (tieba_name, ))
		else:
			print('%s吧签到失败' % (tieba_name, ))

	# 判断贴吧内是否有置顶帖
	if is_element_exist(top_xpath):
		
		tops = browser.find_elements_by_xpath(top_xpath)
		# top_linkText = top.get_attribute("title")
		ToF, top = veryfy(tops)
		if (ToF):
			# 选择置顶帖中的广告集中贴回复
			back_post(top, text)
		else:
			# 选择普通发帖
			print(top)
			# normal_post(title, text)

tieba_post(tieba_name, title, text)


