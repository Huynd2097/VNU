#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import csv

class Student(object):
	"""docstring for Student"""
	def __init__(self):
		pass
		
def get_inputvalue_byname(src, name):
	if not name:
		return ''

	match = re.search('<nobr>' + name + '.*?> (.*?)(\&nbsp;)?</td>', src)
	if not match:
		return ''
	return match.group(1)


def collect_info(src):
	ss = []
	
	ss.append(get_inputvalue_byname(src, 'Mã sinh viên'))
	ss.append(get_inputvalue_byname(src, 'AdditionlClass'))
	ss.append(get_inputvalue_byname(src, 'Họ và tên:'))
	sex = get_inputvalue_byname(src, 'Giới tính:')
	ss.extend(re.findall('(\w+)', sex))
	# print re.findall('(\w+)', sex)
	ss.append(get_inputvalue_byname(src, 'ĐT di động'))
	ss.append(get_inputvalue_byname(src, 'Ngày sinh'))
	ss.append(get_inputvalue_byname(src, 'Số CMT'))
	ss.append(get_inputvalue_byname(src, 'Thư điện tử'))
	ss.append(get_inputvalue_byname(src, 'Nơi ở hiện nay'))
	
	return ss

#overwrite file
def write_file_csv(data, fileName):
	with open(fileName, 'wb') as csvfile:
		csvWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for row in data:
			csvWriter.writerow(row)


	


def claw_ss(folder_path):
	lists = []

	list_file = os.listdir(folder_path)

	for sv_id in list_file:
		file_content = open(folder_path + '\\' + sv_id).read()
		sv_info = collect_info(file_content)
		lists.append(sv_info)
		write_file_csv(lists, 'sol.csv')
		print sv_id

claw_ss('D:\Source_Code\AutoIT\Tshirt\svv')