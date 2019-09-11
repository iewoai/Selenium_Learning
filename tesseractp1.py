from PIL import Image
import pytesseract, os

def IsValidImage(img_path):
	bValid = True
	try:
		Image.open(img_path).verify()
	except:
		bValid = False
		print('无效图片路径')
	return bValid

# 识别效果太差
def text_reco(img_path):
	if IsValidImage(img_path):
		'''
		# 图片格式转化（没啥必要）
		img_name, img_type = os.path.splitext(img_path)
		if img_type != '.jpg':
			img_new_path = img_name + '.jpg'
			try:
				im = Image.open(img_path)
				im.convert('RGB')
				im.save(img_new_path)
			except Exception as e:
				print(e)
			# os.remove(img_path)
			image = Image.open(img_new_path)
		else:
		'''
		image = Image.open(img_path)
		# # 英文
		# # vcode = pytesseract.image_to_string(image, lang='eng')
		# # print(vcode)
		# # 当图片格式为png时无论是识别中文还是英文都会出现utf-8的编码错误
		# # 中文
		text = pytesseract.image_to_string(image, lang='chi_sim')
		return text

img_path = 'F:\\py学习\\selenium\\baidu3.png'
image = Image.open(img_path)
vcode = pytesseract.image_to_string(image, lang='chi_sim')
print(vcode)
# text_reco(img_path)




'''
# 此截图方式不能截取全界面长图
try:
	# 两种方式截图，建议用.png格式，用jpg格式会警告
	browser.get_screenshot_as_file('baidu1.png')
	browser.save_screenshot('baidu2.png')
	print('截图成功')
except Exception as e:
	print('截图失败')
	print(e)
'''

'''
# 使用PhantomJS截长图
browser = webdriver.PhantomJS(executable_path='F:\\py学习\\selenium\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
browser.maximize_window()
browser.get(url)
browser.save_screenshot('baidu3.png')
'''

'''指定元素位置截图
browser.save_screenshot('test.png')
time.sleep(1)
exp1 = browser.find_element_by_id('ftCon')
# 获取元素位置
location = exp1.location
print(location)
left = exp1.location['x']
top = exp1.location['y']
right = exp1.location['x'] + exp1.size['width']
bottom = exp1.location['y'] + exp1.size['height']
test = Image.open('test.png')
testnew = test.crop((left, top, right, bottom))
testnew.save('testnew.png')
'''