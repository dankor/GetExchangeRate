import requests, sys, os
from datetime import datetime,timedelta

def get_rate(Country,CurrencyFrom,CurrencyTo,Date):

	# Supress warnings
	requests.packages.urllib3.disable_warnings() 

	#Fake headers
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36','Connection': 'keep-alive'}
	
	if Country == 'UA' and CurrencyFrom == 'UAH':
		r = requests.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange", params={'valcode': CurrencyTo, 'date': Date.replace('-', '')},headers=headers)
		rate = r.text[r.text.find('<rate>')+6:r.text.find('</rate>')]
		
	if Country == 'RU' and CurrencyFrom == 'RUB':
		r = requests.post('http://www.cbr.ru/scripts/XML_daily.asp', params={'date_req': Date[-2:]+ '/' + Date[5:7] + '/' + Date[:4]},headers=headers)
		rate = r.text[r.text.find(CurrencyTo):]
		rate = rate[rate.find('<Value>')+7:rate.find('</Value>')].replace(',','.')

	if Country == 'BY' and CurrencyFrom == 'BYN':
		r = requests.get('http://www.nbrb.by/API/ExRates/Rates', params={'onDate': Date,'Periodicity': '0'},headers=headers)
		rate = r.text[r.text.find(CurrencyTo):]
		rate = rate[rate.find('"Cur_OfficialRate"')+19:rate.find('},{')]

	if Country == 'PL' and CurrencyFrom == 'PLN':
		r = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/'+ CurrencyTo +'/' + Date + '/?format=json')			
		if r.text.find('"mid":') == -1:			
			rate = get_rate(Country,CurrencyFrom,CurrencyTo,(datetime.strptime(Date, '%Y-%M-%d') + timedelta(days=-1)).strftime("%Y-%M-%d"))
		else:
			rate = r.text[r.text.find('"mid":')+6:r.text.find('}]}')]		

	if Country == 'GE' and CurrencyFrom == 'GEL':
		r = requests.post('https://www.nbg.gov.ge/index.php?m=582&lng=eng', data={'item': 'ALL', 'date_start': Date, 'date_end': Date, 'x':'31', 'y':'7', 'action':'search'},headers=headers, verify=False)
		rate = r.text[r.text.find(CurrencyTo)+3:]
		rate = rate[rate.find(CurrencyTo):]
		rate = rate[rate.find('">')+2:]
		rate = rate[rate.find('">')+2:]
		rate = rate[:rate.find('</td>')].replace(' ','').replace('\n','').strip()

	if Country == 'KZ' and CurrencyFrom == 'KZT' and CurrencyTo == 'USD':
		r = requests.post('https://www.nationalbank.kz/?docid=362&switch=english', data={'docid': '362', 'eDate': Date[-2:]+ '/' + Date[5:7] + '/' + Date[:4], 'flag': '1', 'idval': '5','OK2': 'Show report', 'sDate': Date[-2:]+ '/' + Date[5:7] + '/' + Date[:4]}, verify=False,headers=headers)			
		rate = r.text[r.text.find('US DOLLAR'):]
		rate = rate[rate.find('<td align="center">')+19:]
		rate = rate[rate.find('<td align="center">')+29:]
		rate = rate[:rate.find('</td>')-9].replace(' ','').replace('\n','').strip()		

	if Country == 'AZ' and CurrencyFrom == 'AZN':
		r = requests.get('https://www.cbar.az/currencies/' + Date[-2:]+ '.' + Date[5:7] + '.' + Date[:4] + '.xml')
		rate = r.text[r.text.find(CurrencyTo):]
		rate = rate[rate.find('<Value>')+7:rate.find('</Value>')]

	if Country == 'LT' and CurrencyFrom == 'EUR':
		r = requests.get('http://old.lb.lt/webservices/FxRates/FxRates.asmx/getFxRates', params={'tp': 'EU', 'dt': Date},headers=headers)
		rate = r.text[r.text.find(CurrencyTo):]
		rate = rate[rate.find('<Amt>')+5:rate.find('</Amt>')]

	if Country == 'LV' and CurrencyFrom == 'EUR':
		r = requests.get('https://www.bank.lv/vk/ecb.xml', params={'date':Date.replace('-', '')},headers=headers)
		rate = r.text[r.text.find(CurrencyTo):]
		rate = rate[rate.find('<Rate>')+6:rate.find('</Rate>')]

	if Country == 'EE' and CurrencyFrom == 'EUR':
		r = requests.get('https://www.eestipank.ee/en/historical-exchange-rates', params={'is_ajax':'true', 'chart_start_at':Date[-2:]+ '.' + Date[5:7] + '.' + Date[:4], 'chart_end_at':Date[-2:]+ '.' + Date[5:7] + '.' + Date[:4], 'chart_step':'day', 'currency_code': CurrencyTo},headers=headers)
		rate = r.text		
		if rate.find('"1 EUR = ') == -1:			
			rate = get_rate(Country,CurrencyFrom,CurrencyTo,(datetime.strptime(Date, '%Y-%M-%d') + timedelta(days=-1)).strftime("%Y-%M-%d"))
		else:
			rate = rate[rate.find('"1 EUR = ')+9:]
			rate = rate[:rate.find(' ' + CurrencyTo)]

	if Country == 'UZ' and CurrencyFrom == 'UZS':		
		r = requests.get('https://nbu.uz/exchange-rates/?bxrand=' + str(int(datetime.now().timestamp())),headers=headers)
		print(r.cookies)
		headers.update({'Cookie':'PHPSESSID=' + str(r.cookies.get_dict()['PHPSESSID'])})
		headers.update({'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
		headers.update({'X-Requested-With': 'XMLHttpRequest'})
		sessid = r.text[r.text.find('bitrix_sessid')+16:]
		sessid = sessid[:sessid.find('}')-1]
		rate = requests.post('https://nbu.uz/api/exchange_archive/', data={'date':Date[-2:]+ '.' + Date[5:7] + '.' + Date[:4],'sessid': sessid},headers=headers).text
		rate = rate[rate.find(CurrencyTo):]
		rate = rate[rate.find('<td>')+4:]
		rate = rate[:rate.find('</td>')]

	return(rate)

if len(sys.argv) == 5:
	print(get_rate(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]))
