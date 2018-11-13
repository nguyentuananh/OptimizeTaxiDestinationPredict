import BeautifulSoup
from selenium import webdriver

browser = webdriver.Firefox()
browser.get('https://www.kaggle.com/account/login')

username = browser.find_element_by_id("username-input-text")
password = browser.find_element_by_id("password-input-text")

username.send_keys("")
password.send_keys("")
browser.find_element_by_id("submit-sign-in-button").click()

browser.get("https://www.kaggle.com/c/pkdd-15-predict-taxi-service-trajectory-i/submissions?sortBy=date&group=all&page=1")
doc = BeautifulSoup.BeautifulSoup(browser.page_source)
kvalues = []
for row in doc.findAll("div", { "class" : " competition-submissions__info-text inline-text-editor__readonly" }):
	print row.text
	kvalues.append(row.text)
print '--------'
print kvalues
print '--------'
results = doc.findAll('div', {"class" : "competition-submissions__score"})

f = open("kvalue", "r")
content = f.read()
kvalue = int(content)
f.close()
print kvalue

for idx, val in enumerate(kvalues):
    if int (val) is kvalue:
        result = float(results[2+2*idx].text)
        print "k = %d, result = %.5f" % (kvalue, result)
        f = open("resultvalue","w+")
        f.write("%.5f\r\n" % result)
        f.close()
        break
browser.quit()
