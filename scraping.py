import requests #http request

from bs4 import BeautifulSoup #web scraping

import smtplib # send email

#email body 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#System date and time manipulation
import datetime
now=datetime.datetime.now()

#email content placeholder
content = ''

#Extracting Hacker news stories

def extract_news(url):
    print("Extracting the Hacker News Stories...")
    cnt=''
    cnt+=('<b>HN Top Stories:</b>\n'+'-'*50+'</b>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content,'html.parser')
    for i, tag in enumerate(soup.find_all('td',attrs={'class':'title','valign':''})):
        cnt += ((str(i+1)+' :: '+tag.text + "\n" + '<br>') if tag.text!= 'More' else '' )
    return(cnt)
cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>----------------------<br>')
content += ('<br><br>End of Message')

#Send The Mail

print('Composing the Email.....')

#Email Details

SERVER = 'smtp.gmail.com'  #your smtp server
PORT = 587 #Your port Number
FROM = 'xyz@gmail.com'
TO ='abc@gmail.com'
PASS = 'xyz'

#Create msg body
msg = MIMEMultipart()
msg['Subject'] = 'Top News Stories HN [Automated Email]' + ' ' + str(now.day) + '-' + str(now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))

#Authentication Section
print('Initiating Server...')
server = smtplib.SMTP(SERVER,PORT)
server.set_debuglevel(1) #To get error msg during authentication.If not needed gite value 0
server.ehlo #Initiating the Server
server.starttls()
server.login(FROM,PASS)
server.sendmail(FROM,TO,msg.as_string())

print('Email Send.....')
server.quit()

