from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import sys
from datetime import datetime
from openpyxl import load_workbook

now = datetime.now()
current_time = now.strftime("%m_%d_%H_%M")

browser = webdriver.Chrome()
browser.implicitly_wait(10)
browser.get('https://everytime.kr/')

loginButton = browser.find_element_by_class_name('login')
loginButton.click()

inputId = browser.find_element_by_name('userid')
inputPassword = browser.find_element_by_name('password')

inputId.send_keys('mun97696')
inputPassword.send_keys('munjun03261')
loginSubmitButton = browser.find_element_by_class_name('submit')
loginSubmitButton.click()

boards = browser.find_elements_by_class_name('new')

num = int(input('0: 자유게시판 1: 비밀게시판 2: 졸업생게시판 3: 새내기게시판 4: 시사/이슈    '))
whatIsBoard = boards[num]
whatIsBoard.send_keys(Keys.ENTER)

file = open("{0} {1}.txt".format(num, current_time),"w", encoding="utf8")

if num == 0:
    while True:
        articles = browser.find_element_by_css_selector("div#container.article > div.wrap.articles")
        for i in range(2,22):
            Title = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#container > div.wrap.articles > article:nth-child({}) > a > h2".format(i))))
            Body = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#container > div.wrap.articles > article:nth-child({})".format(i))))

            if(Title.text.find('정통') > 0 or Body.text.find('정통?') > 0):
                Body.click()
                InTitle = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#container > div.wrap.articles > article > a > h2")))
                InBody = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#container > div.wrap.articles > article > a > p")))
                InTime = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#container > div.wrap.articles > article > a > div.profile > time")))
                InCommentCount = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#container > div.wrap.articles > article > a > ul.status.left > li.comment")))

                file.write(InTitle.text + '     ')
                file.write(InTime.text + '\n')
                file.write(InBody.text + '\n')

                if InCommentCount.text == '0':
                    browser.back()
                    file.write('\n')
                    continue
                else:
                    comments = browser.find_elements_by_css_selector("#container > div.wrap.articles > article > div > article")

                for comment in comments:
                    content = comment.find_element_by_tag_name('p')
                    if comment.get_attribute('class') == 'child':
                        file.write("    ")
                    file.write(content.text + '\n')
                file.write('\n')

                # if InTime.text.find('08') >= 0:
                 #   sys.exit("after september")
                browser.back()


        nextButton = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#container > div.wrap.articles > div.pagination > a.next")))
        if nextButton == -1:
            nextButton = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#container > div.wrap.articles > div.pagination > a")))

        nextButton.click()

elif num > 0 and num < 5:
    while True:
        articles = browser.find_element_by_css_selector("div#container.article > div.wrap.articles")
        for i in range(2,22):
            Body = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#container > div.wrap.articles > article:nth-child({})".format(i))))

            if(Body.text.find('정통') > 0):
                Body.click()
                InBody = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#container > div.wrap.articles > article > a > p")))
                InTime = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#container > div.wrap.articles > article > a > div.profile > time")))
                InCommentCount = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#container > div.wrap.articles > article > a > ul.status.left > li.comment")))

                file.write(InBody.text + '        ')
                file.write(InTime.text + '\n')

                if InCommentCount.text == '0':
                    browser.back()
                    file.write('\n')
                    continue
                else:
                    comments = browser.find_elements_by_css_selector("#container > div.wrap.articles > article > div > article")

                for comment in comments:
                    content = comment.find_element_by_tag_name('p')
                    if comment.get_attribute('class') == 'child':
                        file.write("    ")
                    file.write(content.text + '\n')
                file.write('\n')

                # if InTime.text.find('08') >= 0:
                    # sys.exit("after september")
                browser.back()


        nextButton = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#container > div.wrap.articles > div.pagination > a.next")))
        if nextButton == -1:
            nextButton = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#container > div.wrap.articles > div.pagination > a")))

        nextButton.click()
else:
    sys.exit('wrong num')
