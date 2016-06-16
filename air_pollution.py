# -*- coding:utf-8 -*-
#!/usr/bin/python
import urllib2
from bs4 import BeautifulSoup
import  sys 
reload ( sys ) 
sys . setdefaultencoding ( 'utf-8' )
import speech_recognition as sr
r = sr.Recognizer()
sr.energy_threshold = 4000
with sr.Microphone() as source:
    audio = r.listen(source)

request2=urllib2.Request("http://opendata.epa.gov.tw/ws/Data/REWXQA/?$orderby=SiteName&$skip=0&$top=1000&format=xml")
response2=urllib2.urlopen(request2)
html2=response2.read()
soup2=BeautifulSoup(html2,"lxml")

try:
    print("You said " + r.recognize_google(audio,language="zh_TW"))

except sr.UnknownValueError:
    print("Could not understand audio")
word=r.recognize_google(audio,language="zh_TW")
#print word
if word==u'台北市' or u'台中市' or u'台南市': 
	word=word.replace('台', '臺')
	#print word
for data in soup2.find_all('data'):
	#x="data.'pm2.5'.text"
	dict={"County":data.county.text,"SiteName":data.sitename.text,"PSI":data.psi.text,"PM10":data.pm10.text,
		  "Status":data.status.text,"PublishTime":data.publishtime.text}
		
	if dict["SiteName"]==word:
		print "["+dict["County"]+','+dict["SiteName"]+']=>'+u'[空氣狀態為',dict[u'Status']+'],'+'[空氣汙染指標為',dict['PSI']+'],'+"[PM10為",dict['PM10']+']'
	elif dict["County"]==word:
		print "["+dict["County"]+','+dict["SiteName"]+']=>'+u'[空氣狀態為',dict[u'Status']+'],'+'[空氣汙染指標為',dict['PSI']+'],'+"[PM10為",dict['PM10']+']'


