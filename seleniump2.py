from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import chardet, time
browser = webdriver.Firefox()
browser.get(r'https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2F2.taobao.com%2F')
# 根据链接内容找到元素
time.sleep(0.2)
browser.maximize_window()
wait = WebDriverWait(browser, 10)
wait.until(EC.presence_of_element_located((By.ID,'J_Quick2Static')))


user_name = "teacup12138"
user_password = "2016xiaowei"
# 点击登陆xpath
clogin_xpath = "//div[@class='login-switch']"
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
sign_in()
time.sleep(0.5)
login_button = browser.find_element_by_xpath(login_xpath)
login_button.click()