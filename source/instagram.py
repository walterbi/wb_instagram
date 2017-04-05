from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import os, time, sys
import urllib


def insta_login(__username__, __password__):
	# checking loading site
	for i in xrange(sys.maxint):
		checking_flag = False
		driver.get("https://www.instagram.com/")
		img_app = driver.find_elements_by_tag_name("img")
		for elm_im_app in img_app:
			alt = elm_im_app.get_attribute("alt")
			if alt == "Available on Google Play":
				print "[+] Login page loading completed."
				checking_flag = True

		if checking_flag:
			break

	WebDriverWait(driver, 60).until(
		EC.presence_of_element_located((By.TAG_NAME, "input"))
		)

	# Find login link to click on
	login_links = driver.find_elements_by_tag_name("a")
	for elm_login_link in login_links:
		inner_text = elm_login_link.text
		print inner_text
		if inner_text == "Log in":
			print "[+] Login link founded."
			elm_login_link.click()
			print "[+] Login link clicked."
	# return driver

	# Find login element to fill
	input_raw = driver.find_elements_by_tag_name("input")
	for elm_input_raw in input_raw:
		elm_name = elm_input_raw.get_attribute("name")
		if elm_name == "username":
			elm_input_raw.send_keys(__username__)
			print "[+] Username sent."
		if elm_name == "password":
			elm_input_raw.send_keys(__password__)
			print "[+] Password sent."
	input_button = driver.find_element_by_tag_name("button")
	input_button.click()
	print "[+] Login pressed."


def insta_download(__user__, __required__, __total__):

	for i in xrange(sys.maxint):

		checking_flag = False
		driver.get("https://www.instagram.com/" + __user__)

		load_more = driver.find_elements_by_tag_name("a")
		for elm_load_more in load_more:
			inner_text = elm_load_more.text
			if inner_text == "Load more":
				print "[+] Load more founded."
				checking_flag = True
				break
		if checking_flag:
			print "[+] User page loaded."
			break

	# Loading depend on required post
	if __required__ <= 12 and __required__ != 0:
		# do nothing
		print "[+] Smaller than 1 page."

	if __required__ > 12:
		# Click to load more
		load_more = driver.find_elements_by_tag_name("a")
		for elm_load_more in load_more:
			inner_text = elm_load_more.text
			if inner_text == "Load more":
				print "[+] Load more founded."
				elm_load_more.click()
				break

		# Begin loading
		count_float = (__required__ - 24) / 11
		for i in range(count_float):
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			wait_str = "[+] Wait: " + str(i + 1)
			sys.stdout.write("\r" + wait_str)
			sys.stdout.flush()
			time.sleep(2)
		print ""

	if __required__ == 0:
		# Click to load more
		load_more = driver.find_elements_by_tag_name("a")
		for elm_load_more in load_more:
			inner_text = elm_load_more.text
			if inner_text == "Load more":
				print "[+] Load more founded."
				elm_load_more.click()
				break

		# Begin loading
		count_float = (__total__ - 24) / 11
		for i in range(count_float):
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			wait_str = "[+] Wait: " + str(i + 1)
			sys.stdout.write("\r" + wait_str)
			sys.stdout.flush()
			time.sleep(2)
		print ""


	insta_imgs = driver.find_elements_by_tag_name("img")
	count_percent = 0
	for elm_insta_img in insta_imgs:
		img_name = ""
		elm_id = elm_insta_img.get_attribute("id")
		if "pImage" in elm_id:
			img_src = elm_insta_img.get_attribute("src")
			tmp_split = img_src.split("/")
			img_name = tmp_split[len(tmp_split) - 1].split("?")[0]
			# print "[+] " + img_name

			# Re-construct source link
			re_source = []
			__count__ = 0
			src_len = len(tmp_split)
			while __count__ < src_len:
				if tmp_split[__count__] == "s640x640":
					__count__ += 2
				if tmp_split[__count__] != "s640x640":
					re_source.append(tmp_split[__count__])
					__count__ += 1

			# Saving file
			img_src = "/".join(re_source)
			urllib.urlretrieve(img_src, os.getcwd() + "/" + __user__ + "/" + img_name)
			
			count_percent += 1
			if __required__ == 0:
				percent_str = "[+] Completed: " + str(count_percent) + " / " + str(__total__)
			else:
				percent_str = "[+] Completed: " + str(count_percent) + " / " + str(__required__)
			sys.stdout.write("\r" + percent_str)
			sys.stdout.flush()
	print ""


def insta_total(__user__):

	for i in xrange(sys.maxint):

		checking_flag = False
		driver.get("https://www.instagram.com/" + __user__)

		load_more = driver.find_elements_by_tag_name("a")
		for elm_load_more in load_more:
			inner_text = elm_load_more.text
			if inner_text == "Load more":
				print "[+] Load more founded."
				checking_flag = True
				break
		if checking_flag:
			print "[+] User page loaded."
			break

	user_header = driver.find_element_by_tag_name("header")
	user_li = user_header.find_elements_by_tag_name("li")[0]
	return int(user_li.get_attribute("innerHTML").split(">")[4].split("<")[0])


if __name__ == "__main__":

	try:
		insta_account = raw_input("[+] Enter instagram account: ")

		driver = webdriver.Firefox()
		
		total_post = insta_total(insta_account)
		# Check download folder
		if not os.path.isdir(insta_account):
			os.mkdir(insta_account)

		print "[+] Total post: " + str(total_post)

		required_post = int(raw_input("[+] Enter total post to load (0 = all): "))

		insta_download(insta_account, required_post, total_post)
		
		os.system("pkill firefox")
		os.system("pkill geckodriver")

	except Exception as err:
		os.system("pkill geckodriver")
		print "[+] geckodriver killed."
		raise err
		
