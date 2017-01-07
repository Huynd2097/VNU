import requests
import time
import thread
import re 	#regex
import sys 	#input

def main():
	msv = ''
	passwd = ''
	listClassId = ['MAT1093 4', 'HIS1002 5', 'PHY1103 2']
	dkmk = DkmhVnu(msv, passwd)
	dkmk.changeClass('cancel', listClassId)
	while dkmk.threadActive:
		pass

	


class DkmhVnu(object):
	"""Dang ky mon hoc cua DHQG HN"""
	urlLogin = 'http://dangkyhoc.vnu.edu.vn/dang-nhap'
	urlSelect = 'http://dangkyhoc.vnu.edu.vn/chon-mon-hoc/' # + rowindex + '/1/1'
	urlCancel= 'http://dangkyhoc.vnu.edu.vn/huy-mon-hoc/'	# + rowindex + '/1/1'
	urlConfirm = 'http://dangkyhoc.vnu.edu.vn/xac-nhan-dang-ky/1'
	urlSchoolList = 'http://dangkyhoc.vnu.edu.vn/danh-sach-mon-hoc/1/1'
	urlYourList = 'http://dangkyhoc.vnu.edu.vn/danh-sach-mon-hoc-da-dang-ky/1'
	urlPageReg = 'http://dangkyhoc.vnu.edu.vn/dang-ky-mon-hoc-nganh-1'
	# urlCheck = 'http://dangkyhoc.vnu.edu.vn/kiem-tra-tien-quyet/' # + id + '/1'

	threadActive = 0

	def __init__(self, loginName, password):
		super(DkmhVnu, self).__init__()
		self.__loginName = loginName
		self.__password = password

		print 'Trying to login...'
		self.__mainSession = self.login()
		if self.__mainSession:
			print 'Logged in! (', self.__loginName, ')'
		else:
			print 'Wrong loginName (', self.__loginName, ') or password (', '*' * len(self.__password), ')'

		# print self.__mainSession.post(self.urlYourList).text
		

	#return '' if fail
	def login(self):
		if not self.__loginName or not self.__password:
			return ''

		sess = requests.session()
		
		token = ''
		while 1:
			#get token
			if not token:
				match = re.search( '__RequestVerificationToken" type="hidden" value="(.*?)"', sess.get(self.urlLogin).text)
				if not match:
					continue

				token = match.group(1)
			
			#post data
			data = {'__RequestVerificationToken' : token, 'loginName' : self.__loginName, 'password' : self.__password}
			response = sess.post(self.urlLogin, data=data).text
			if 'Sai t' in response:
				return ''
			if 'Logout' in response:
				
				sess.headers.update({'referer': self.urlPageReg})
				return sess

	#mode: register || cancel
	# listClassId: danh sach ma lop mon hoc
	def changeClass(self,mode, listClassId):
		if not self.__mainSession:
			print mode, 'ERROR: You are not logged in'
			return

		for classId in listClassId:
			if mode == 'register':
				thread.start_new_thread(self.__process_register, (classId,))
			elif mode == 'cancel':
				thread.start_new_thread(self.__process_cancel, (classId,))
			else:
				print 'Unknow mode!'

		time.sleep(1)

	def __get_class_index(self, classId, session, retry=True, registered=False):
		if not session:
			print classId, ': ERROR Get index'
			return ''
		urlList = self.urlSchoolList
		pattern = '(?s)\<tr(.*?)\<\/tr'
		if registered:
			urlList = self.urlYourList
			pattern = '(?s)\<tr class="registered"(.*?)\<\/tr'

		while 1:
			sourceListReg = session.post(urlList).text
			for row in re.findall(pattern, sourceListReg):
				if classId in row:
					mIndex = re.findall('data-rowindex="(.*?)"', row)
					if mIndex:
						return mIndex[0]		
			
			if not retry:
				return ''

			time.sleep(0.1)

		
	def __process_cancel(self, classId):
		self.threadActive += 1
		sess = self.login()

		if sess and classId in sess.post(self.urlYourList).text:
			classIndex = self.__get_class_index(classId, sess, registered=True)

			if classIndex:				
				print classId, ': Trying to remove...'

				while 1:
					sess.post(self.urlSchoolList)
					sess.post(self.urlYourList)

					sess.post(self.urlCancel + classIndex + '/1/1')

					sess.post(self.urlSchoolList)
					sess.post(self.urlYourList)
					
					sess.post(self.urlConfirm)
					if not classId in sess.post(self.urlYourList).text:
						print classId, ': Canceled'

						self.threadActive -= 1
						return ''

		print classId, ': Cancel ERROR'
		self.threadActive -= 1
		return ''

	def __process_register(self, classId):
		self.threadActive += 1
		sess = self.login()

		if not sess or classId in sess.post(self.urlYourList).text:

			classIndex = self.__get_class_index(classId, sess)
			if not classIndex:			
				print classId, ': Trying to register...'

				while 1:
					sess.post(self.urlSelect + classIndex + '/1/1')
					sess.post(self.urlConfirm)
					if self.__get_class_index(classId, sess, retry=False, registered=True):
						print classId, ': registered'

						self.threadActive -= 1
						return ''

		print classId, ': Register ERROR'
		self.threadActive -= 1
		return ''



if __name__ == '__main__':
    main()
