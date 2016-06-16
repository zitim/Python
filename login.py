import requests
from lxml import html #lxml為python解析html的函式庫

USERNAME = "123"
PASSWORD = "123"

LOGIN_URL = "https://bitbucket.org/account/signin/?next=/"
URL = "https://bitbucket.org/dashboard/overview"
def main():
    session_requests = requests.session()

    # Get login csrf token (Cross Site Request Forgery 跨網站偽造請求)
    result = session_requests.get(LOGIN_URL)
    tree = html.fromstring(result.text)#解析html
    token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]
	#xpath是把網頁裡html碼文件中找需要的內容
                            
    #建立payload
    payload = {
        "username": USERNAME,
        "password": PASSWORD,
        "csrfmiddlewaretoken": token
    }

    #執行登入
    result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))

    # 抓取網站內容
    result = session_requests.get(URL, headers = dict(referer = URL))
    tree = html.fromstring(result.content)
    elems = tree.findall(".//a[@class='execute repo-list--repo-name']")
	# findall(必須是相對路徑.//開頭)，返回匹配結果的所有元素，是一個list
    names = [elems.text_content() for elems in elems]

    print names

if __name__ == '__main__':
     main()
