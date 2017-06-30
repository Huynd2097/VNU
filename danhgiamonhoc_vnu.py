import requests
import re

URL_LOGIN = 'https://courses.uet.vnu.edu.vn/login/index.php'
URL_LIST_COURSE = 'https://courses.uet.vnu.edu.vn/my/index.php?mynumber=-2' # full


def main():
	username = ''
	password = ''
	choice = 4 # choice = 0..4
	dgmh(username, password, choice)


# return Session if login successfully
def login_course(username, password):
	sess = requests.Session()
	data = {
		'username' : username,
		'password' : password,
		'rememberusername' : 1,
	}
	sess.get(URL_LOGIN)
	if not 'logout.php' in sess.post(URL_LOGIN, data=data).content:
		print 'Wrong username or password!'
		return False
	return sess

def get_list_course_urls(sess):
	if not isinstance(sess, requests.Session):
		return False
	source = sess.get(URL_LIST_COURSE).content
	urls = re.findall('http.{20,30}/course/view.php\?id=\d+', source)
	urls = list(set(urls)) # remove duplicate
	return urls

def get_list_questionnaire_urls(sess, course_urls):
	if not isinstance(sess, requests.Session):
		return False
	questionnaire_urls = []
	for url in course_urls:
		source = sess.get(url).content
		match_q = re.search('http.{20,30}mod/questionnaire/view.php\?id=\d+', source)
		if not match_q:
			continue # none questionnaire
		q_url = match_q.group(0)
		source = sess.get(q_url).content
		if 'questionnaire/myreport.php' in source:
			continue # completed
		q_url = q_url.replace('view', 'complete')
		questionnaire_urls.append(q_url)
	return questionnaire_urls


def complete_questionnaire_urls(sess, q_url, choice):
	choice = int(choice) % 5
	source = sess.get(q_url).content
	data = {}
	match_input = re.findall('<input type=".*?name="(.*?)" value="(.*?)"', source)
	for name_value in match_input:
		namen, value = name_value
		data[namen] = value

	# questionnaire
	match_q_id = re.findall('<input name="(q.*?)"', source)
	if not match_q_id:
		return False
	q_ids = set(match_q_id)
	for q_id in q_ids:
		data[q_id] = choice

	sess.post(q_url, data=data)
	print 'Completed id='+ ''.join(re.findall('\d+', q_url))
	return True


def dgmh(username, password, choice=4):
	sess = login_course(username, password)
	if not sess:
		return False
	course_urls = get_list_course_urls(sess)
	questionnaire_urls = get_list_questionnaire_urls(sess, course_urls)
	for q_url in questionnaire_urls:
		complete_questionnaire_urls(sess, q_url)

if __name__ == '__main__':
	main()
