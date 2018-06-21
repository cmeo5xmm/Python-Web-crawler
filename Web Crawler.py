from argparse import ArgumentParser
import requests
import re
from lxml import html
from bs4 import BeautifulSoup as bs
import pytesseract
from PIL import Image,ImageEnhance
from prettytable import PrettyTable
import getpass  

parser = ArgumentParser(description="Web crawler for NCTU class Schedule")
parser.add_argument("username", help="username of NCTU portal")
args = parser.parse_args()
studentid=args.username
pwd = getpass.getpass('Portal Password: ')  
#studentid = '0656095'
#pwd = ''
LOGIN_URL = 'https://portal.nctu.edu.tw/portal/login.php'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36', 
           'Connection': 'keep-alive'}

########try to login
check=0
while check==0:
    #catch graph
    session_requests = requests.session()
    response1 = session_requests.get(url='https://portal.nctu.edu.tw/captcha/pic.php', headers=headers)
    response1.encoding = 'utf-8'

    with open('code.jpg','wb') as fp:
        fp.write(response1.content)
    img=Image.open('code.jpg')
    
    #solve graph
    img_grey = img.convert('L')

    brightness =ImageEnhance.Brightness(img_grey)
    bright_img =brightness.enhance(1.5)

    contrast =ImageEnhance.Contrast(bright_img)
    contrast_img =contrast.enhance(2.0)

    contrast_img.save("after.jpg")
    #image=Image.open('after.jpg')
    number = pytesseract.image_to_string(contrast_img)

    #login
    payload = {
                'username': studentid,
                'password': pwd,
                'pwdtype':'static',
                'seccode' : number
            }
    result = session_requests.post(url='https://portal.nctu.edu.tw/portal/chkpas.php',data = payload ,headers=headers)
    result.encoding = 'utf-8'
    if result.url=="https://portal.nctu.edu.tw/LifeRay/PortalMain.php" :
        check=1

######After login
re1 = session_requests.get(url='https://portal.nctu.edu.tw/portal/relay.php?D=cos', headers=headers)
re1.encoding = 'utf-8'
tree = html.fromstring(re1.text)
txtId = list(set(tree.xpath('//input[@name="txtId"]/@value')))[0]
txtPw = list(set(tree.xpath('//input[@name="txtPw"]/@value')))[0]
ldapDN = list(set(tree.xpath('//input[@name="ldapDN"]/@value')))[0]
idno = list(set(tree.xpath('//input[@name="idno"]/@value')))[0]
s = list(set(tree.xpath('//input[@name="s"]/@value')))[0]
t = list(set(tree.xpath('//input[@name="t"]/@value')))[0]
time=list(set(tree.xpath('//input[@name="txtTimestamp"]/@value')))[0]
hashkey= list(set(tree.xpath('//input[@name="hashKey"]/@value')))[0]
jwt = list(set(tree.xpath('//input[@name="jwt"]/@value')))[0]
payload = {
                'txtId':txtId,
                'txtPw': txtPw,
                'ldapDN':ldapDN,
                'idno':idno,
                's':s,
                't':t,
                'txtTimestamp':time,
                'hashKey':hashkey,
                'jwt':jwt,
                'Chk_SSO':'on'
            }
course = session_requests.post(url='https://course.nctu.edu.tw/jwt.asp',data = payload )
course = session_requests.get(url='https://course.nctu.edu.tw/adSchedule.asp', headers=headers)
course.encoding = 'big5'
soup = bs(course.text, 'html.parser')


l=[]
table = soup.find_all('td')
for inside in table:
    l.append(inside.get_text())

x=0
while x<len(l) :
    l[x]= ''.join(l[x].split())
    x=x+1

tab=PrettyTable(padding_width=2)
tab.field_names = ["節次","時間\星期","(一)","(二)","(三)","(四)","(五)","(六)","(日)",]
x=12
while x<150 :
    tab.add_row( [l[x],l[x+1],l[x+2],l[x+3],l[x+4],l[x+5],l[x+6],l[x+7],l[x+8]])
    x=x+9
tab.align="c"
print(tab)