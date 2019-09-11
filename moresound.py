from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import chardet, time, random, re, os, pickle
from PIL import Image

url = 'http://moresound.tk/music/'
head_id = 'tipsDay'
search_id = 'search_input'
type_id = 'search_type'
name = '周杰伦'
type_xpath = '//div[@data-type="mg"]'
song_xpath = '//li[@class="song_item"]'
jay = []
path = 'jay.p'

browser = webdriver.Chrome()
# driver = webdriver.PhantomJS(executable_path='F:\\py学习\\selenium\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')

# browser.maximize_window()
browser.get(url)

'''
# 在chrome使用改变窗口大小的方式截全屏图，失败
# scroll_width = browser.execute_script('return document.body.parentNode.scrollWidth')
# print(scroll_width)

# scroll_height = browser.execute_script('return document.body.parentNode.scrollHeight')
# print(scroll_height)

# browser.set_window_size(scroll_width, scroll_height)
# browser.save_screenshot('baidu4.png')
'''

wait = WebDriverWait(browser, 60)
wait.until(EC.presence_of_element_located((By.ID, head_id)))
browser.find_element_by_id(head_id).click()
time.sleep(0.5)

browser.find_element_by_id(type_id).click()
time.sleep(0.2)
browser.find_element_by_xpath(type_xpath).click()

search = browser.find_element_by_id(search_id)
search.click()
search.send_keys(name)
search.send_keys(Keys.ENTER)

wait = WebDriverWait(browser, 60)
wait.until(EC.presence_of_element_located((By.XPATH, song_xpath)))
# try:
# 	while True:
# 		time.sleep(5)
# 		js = "document.getElementById('MS_search_result').scrollTo(0,20000)"
# 		browser.execute_script(js)

# 		wait = WebDriverWait(browser, 60)
# 		wait.until(EC.visibility_of_element_located((By.ID, 'msgTips')))
# except Exception as e:
# 	print(e)

while True:
	time.sleep(5)
	print('手动加载所有歌曲：')
	song_list = browser.find_elements_by_xpath(song_xpath)
	print(len(song_list))
	if len(song_list) > 200:
		break

song_name_list = browser.find_elements_by_xpath('//h6[@class="song_name"]')
song_acoustic = browser.find_elements_by_xpath('//h6[@class="song_name"]/sup[1]')
song_album = browser.find_elements_by_xpath('//h6[@class="song_name"]/sup[last()]')
song_singer = browser.find_elements_by_xpath('//p[@class="singer_name"]')
print('共有%d个结果' % len(song_name_list))

for i, song_name in enumerate(song_name_list):
	name = song_name.get_attribute('textContent')
	acoustic = song_acoustic[i].get_attribute('textContent')
	album = song_album[i].get_attribute('textContent')
	singer = song_singer[i].get_attribute('textContent')
	name = re.sub(acoustic, '', name)
	name = re.sub(album, '', name)
	mp3_url = ''
	song_name.click()
	# print(name, singer, acoustic, album)
	wait = WebDriverWait(browser, 60)
	wait.until(EC.presence_of_element_located((By.XPATH, '//a[@class="close_song_download_page"]')))
	link_list = browser.find_elements_by_id('song_link')
	for link in link_list:
		acou = link.get_attribute('textContent')
		if acou == '320MP3':
			mp3_api = url + link.get_attribute('src')
			print(browser.current_url)
			js = 'window.open("%s");' % mp3_api
			browser.execute_script(js)
			top_handle = browser.current_window_handle
			handles = browser.window_handles
			for handle in handles:
				if handle != top_handle:
					back_handle = handle
			browser.switch_to.window(back_handle)
			print(browser.current_url)
			print(browser.page_source)
			code = re.findall('"code":(.*?),', browser.page_source)[0]
			if code != 0:
				mp3_url = re.findall('"url":"(.*?)",', browser.page_source)[0]
				print(mp3_url)
			else:
				print('请求错误')
			browser.close()
			browser.switch_to.window(top_handle)
			break
			time.sleep(3)
	browser.find_element_by_xpath('//a[@class="close_song_download_page"]').click()
	print(name, singer, acoustic, album, mp3_url)
	song_data = {
		'name': name,
		'singer': singer,
		'acoustic': acoustic,
		'album': album,
		'320mp3': mp3_url,
	}
	jay.append(song_data)

print(jay)
with open(path, 'wb') as f:
	pickle.dump(jay, f)

