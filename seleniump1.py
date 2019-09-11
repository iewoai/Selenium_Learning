
# 初始例子
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import chardet, time, random
import re, os
# 创建chrome浏览器对象
browser = webdriver.Chrome()
'''打开百度并搜索Python，打印输出源代码
try:
	browser.get('https://www.baidu.com')

	# 找到id为kw的元素
	input = browser.find_element_by_id('kw')
	# 敲入python
	input.send_keys('Python')
	# 敲入回车
	input.send_keys(Keys.ENTER)
	# 等待加载
	wait = WebDriverWait(browser, 10)
	# 直到conten_left元素加载出来
	wait.until(EC.presence_of_element_located((By.ID,'content_left')))
	# 打印当前url
	print(browser.current_url)
	# 打印cookis
	print(browser.get_cookies())
	# 打印源码
	s = browser.page_source.encode('utf-8')
	# 调整编码
	print(chardet.detect(s))
	print(s)
	# print(s)
finally:
	# 关闭浏览器对象
	browser.close()
'''

'''跳转和无登陆条登陆
browser.get('https://2.taobao.com/')
# 窗口最大显示
browser.maximize_window()
# 根据链接内容找到元素
login_link = browser.find_element_by_link_text('请登录')
login_link.click()
time.sleep(2)
sign_in = browser.find_element_by_xpath("//div[@class='login-switch']")
sign_in.click()
name = browser.find_element_by_xpath("//input[@type='text']")
name.send_keys('17376500465')
time.sleep(1)
password = browser.find_element_by_xpath("//input[@type='password']")
password.send_keys('2016xiaowei')
submit = browser.find_element_by_xpath("//button[@type='submit']")
submit.click()
time.sleep(3)
browser.close()
'''

# 滑动百度搜索结果滚轴
browser.get('https://www.baidu.com')
input = browser.find_element_by_id('kw')
input.send_keys('Python')
browser.maximize_window()
# 清空input栏
input.clear()
input.send_keys('Java')
button = browser.find_element_by_id('su')
button.click()
# 执行script语句
js = "window.scrollTo(0,document.body.scrollHeight)"
browser.execute_script(js)
time.sleep(1)
js = "window.scrollTo(0,0)"
browser.execute_script(js)
time.sleep(1)
browser.execute_script('alert("结束")')
# time.sleep(1)

# 随机轨迹方法
# def get_track(distance):
# 	track = []
# 	current = 0
# 	mid = distance*3/4
# 	t = random.randint(2,3)/10
# 	v = 0
# 	while current < distance:
# 		if current < mid:
# 			a = 2
# 		else:
# 			a = -3
# 		v0 = v
# 		v = v0+a*t
# 		move = v0*t+1/2*a*t*t
# 		current += move
# 		track.append(round(move))
# 	return track


# 滑动登陆淘宝，失败，原因selenium判定

# 模拟人拉动滑块轨迹
browser.get(r'https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2F2.taobao.com%2F')
# 根据链接内容找到元素
time.sleep(0.2)
browser.maximize_window()
wait = WebDriverWait(browser, 10)

# 可用By.XPATH,"//*[@id='nr']/option[1]"
wait.until(EC.presence_of_element_located((By.ID,'J_Quick2Static')))
# browser.refresh()
# time.sleep(0.2)

# 滑块
# 测试记录手动操作滑块的轨迹(操作十次，然后全部存入本地文件)
# 
a = []
offset = 1
user_name = "teacup12138"
user_password = "2016xiaowei"
text = "dis.text"
# 点击登陆xpath
clogin_xpath = "//div[@class='login-switch']"
# 滑块按钮xpath
slip_xpath = "//span[@id='nc_1_n1z']"
# 刷新xpath
refresh_xpath = "//div[@class='errloading']"
# 登陆按钮xpath
login_xpath = "//button[@id='J_SubmitStatic']"
# 用户名xpath
name_xpath = "//input[@type='text']"
# 用户密码xpath
pass_xpath = "//input[@type='password']"
# 初步登陆
def sign_in():
	sign_in = browser.find_element_by_xpath(clogin_xpath)
	sign_in.click()
	name = browser.find_element_by_xpath(name_xpath)
	name.send_keys(user_name)
	time.sleep(2)
	password = browser.find_element_by_xpath(pass_xpath)
	password.send_keys(user_password)

	time.sleep(2)
# 储存本地文件
def arr_store(a):
	with open(text, "w+") as f:
		try:
			for i in a:
				str = ' '.join(i) +'\n'
				f.write(str)
		finally:
			f.close()

# 从本地提取轨迹
def arr_open():
	with open(text, "r") as f:
		try:
			a = []
			while True:
				text_line = f.readline()
				if text_line:
					b = text_line.strip('\n').split(" ")
					a.append(b)
				else:
					break
		finally:
			return a
			f.close()


# 判断元素是否存在
def is_element_exist(xpath):
	try:
		browser.find_element_by_xpath(xpath)
		return True
	except:
		return False

# 递归10次，将每一次的轨迹存入text
def get_distance():
	global a
	global offset
	if not offset > 10:
		if is_element_exist(slip_xpath):
			print("开始第%d次采集，请滑动滑块" %(offset, ))
			offset += 1
			slip = browser.find_element_by_xpath(slip_xpath)
			try:
				b = []
				while(slip.is_displayed()):
					left = slip.get_attribute("style")
					if(left != ''):
						dis = re.findall(r'\d+', left)[0]
						# print(int(dis))
						b.append(dis)
					time.sleep(0.05)
			except:
				a.append(b)
				time.sleep(0.5)
				get_distance()
		elif(is_element_exist(refresh_xpath)):
			refresh = browser.find_element_by_xpath(refresh_xpath)
			refresh.click()
			get_distance()

	else:
		print('十次人工操作轨迹采集完毕')
# 滑块移动
def move(track_list):
	tab = ActionChains(browser)
	slip = browser.find_element_by_xpath(slip_xpath)
	tab.click_and_hold(slip).perform()
	time.sleep(0.2)
	for i in range(len(track_list)):
		try:
			if i == 0:
				track = int(track_list[i])
			else:
				track = int(track_list[i]) - int(track_list[i-1])
			tab.move_by_offset(xoffset = track, yoffset = 0).perform()
			time.sleep(0.05)
		except:
			break
sign_in()
if not os.path.exists(text): 
	get_distance()
	arr_store(a)
a = arr_open()
track_list = random.choice(a)
move(track_list)
def try100():
	global offset
	if offset < 100:
		if is_element_exist(refresh_xpath):
			login_button = browser.find_element_by_xpath(login_xpath)
			login_button.click()
			time.sleep(2)
			password = browser.find_element_by_xpath(pass_xpath)
			password.send_keys(user_password)
			track_list = random.choice(a)
			move(track_list)
			time.sleep(1)
		try100()
	offset += 1
try100()



# # 修改webdriver，仍然失败，手动console修改登陆成功
# js = r'Object.defineProperties(navigator,{webdriver:{get:() => false}});'
# browser.execute_script(js)

# distance = 258
# track_list=get_track(distance)
# time.sleep(2)

# tab.click_and_hold(slip).perform()
# time.sleep(0.2)

# # 根据轨迹拖拽滑块
# for track in track_list:
# 	try:
# 		tab.move_by_offset(xoffset = track, yoffset = 0).perform()
# 	except:
# 		break


# imitate = tab.move_by_offset(xoffset=-1, yoffset=0)

# time.sleep(0.015)
# imitate.perform()
# time.sleep(random.randint(6,10)/10)
# imitate.perform()
# time.sleep(0.04)
# imitate.perform()
# time.sleep(0.012)
# imitate.perform()
# time.sleep(0.019)
# imitate.perform()
# time.sleep(0.033)

# tab.move_by_offset(xoffset=1, yoffset=0).perform()

# 放开按钮
# tab.pause(random.randint(6,14)/10).release(slip).perform()

# tab.drag_and_drop_by_offset(slip, 258, 0).perform()
# tab.move_to_element(slip).release()
