import requests, time, re, sys
from bs4 import BeautifulSoup
from time import sleep

# Add these values
API_KEY = ''  # Your 2captcha API KEY
site_key = '6LcQOCgUAAAAAIBDpzF5mDmI-ruxkr-8d7G0KHAv'  # site-key, read the 2captcha docs on how to get this
url = 'https://vt.ncsbe.gov/RegLkup/'  # url of page
#proxy = '127.0.0.1:6969'  # example proxy

#proxy = {'http': 'http://' + proxy, 'https': 'https://' + proxy}

s = requests.Session()

# here we post site key to 2captcha to get captcha ID (and we parse it here too)
captcha_id = s.post("http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(API_KEY, site_key, url)).text.split('|')[1]
# then we parse gresponse from 2captcha response
recaptcha_answer = s.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
print("solving ref captcha...")
while 'CAPCHA_NOT_READY' in recaptcha_answer:
    sleep(5)
    recaptcha_answer = s.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
print(recaptcha_answer)
recaptcha_answer = recaptcha_answer.split('|')[1]

print("North Carolina Voter Registry Lookup Tool")

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

#retrieve token needed
verification_soup = BeautifulSoup(requests.get(url).text, 'lxml')
verification_token = verification_soup.find('input',{'name' : '__RequestVerificationToken'}).get('value')
print(verification_token)

#data fields to post
payload = {
	'__RequestVerificationToken' : verification_token,
	'g-recaptcha-response' : recaptcha_answer,
    'FirstName' : 'John',
    'MiddleInitial' : '',
    'LastName' : 'Smith',
    'BirthYear' : '',
    'SelectedCountyID' : '',
    'RegistrationStatusList[0].Name' : 'Registered'
}

#parse data of returned data
source = requests.post(url, payload, headers = headers).text
soup = BeautifulSoup(source, 'lxml')
print(soup.prettify())
