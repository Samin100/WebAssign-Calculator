from selenium import webdriver
from bs4 import BeautifulSoup
from pw import pw  # password stored in separate file


#WebAssign credentials
user = 'sshameem'
pw = pw  #replace this with your actual password

print('Loading browser...')
url = 'https://www.webassign.net/umd/login.html'
browser = webdriver.Chrome()

print('Logging in...')
browser.get(url)

button = browser.find_element_by_id('loginbtn')
button.click()

user_field = browser.find_element_by_id('username')
pw_field = browser.find_element_by_id('password')
submit = browser.find_element_by_class_name('btn-submit')

user_field.send_keys(user)
pw_field.send_keys(pw)
submit.click()

print('Calculating scores...')

# xPath needs to be fixed: change from absolute path to dynamic path
xpath = '//*[@id="webAssign"]/div[2]/div[4]/div[1]/div[1]/div[2]/div[4]/p/a/strong'  
past_assignments = browser.find_element_by_xpath(xpath)
past_assignments.click()

score_page = browser.page_source
score_page_soup = BeautifulSoup(score_page, 'lxml')

scores = score_page_soup.find_all('div', {'class': 'scoreBox'})

assignment_count = 0
score_vals = []


for score in scores:
    assignment_count += 1
    score = score.find('strong').text
    score_raw = score.split(' ')

    if score_raw[1] == '0':
        score_vals.append(0)
    else:
        percentage_raw = score_raw[5]
        percentage = percentage_raw.split('%')
        percentage = percentage[0][1::]
        score_vals.append(float(percentage))


total = 0
for score in score_vals:
    total += score

average = total / assignment_count
average = round(average, 2)

print('Your WebAssign average is ' + str(average) + '%')
browser.close()
