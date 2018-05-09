import requests
import sys
from datetime import datetime,timedelta

def get_rate(Country,CurrencyFrom,CurrencyTo,Date):
	if Country == 'UA' and CurrencyFrom == 'UAH':
		r = requests.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange", params={'valcode': CurrencyTo, 'date': Date.replace('-', '')})
		rate = r.text[r.text.find('<rate>')+6:r.text.find('</rate>')]
		
	if Country == 'RU' and CurrencyFrom == 'RUB':
		r = requests.get('http://www.cbr.ru/scripts/XML_daily.asp', params={'date_req': Date[-2:]+ '/' + Date[5:7] + '/' + Date[:4]})
		rate = r.text[r.text.find(CurrencyTo):]
		rate = rate[rate.find('<Value>')+7:rate.find('</Value>')].replace(',','.')

	if Country == 'BY' and CurrencyFrom == 'BYN':
		r = requests.get('http://www.nbrb.by/API/ExRates/Rates', params={'onDate': Date,'Periodicity': '0'})
		rate = r.text[r.text.find(CurrencyTo):]
		rate = rate[rate.find('"Cur_OfficialRate"')+19:rate.find('},{')]

	if Country == 'PL' and CurrencyFrom == 'PLN':
		r = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/'+ CurrencyTo +'/' + Date + '/?format=json')			
		if r.text.find('"mid":') == -1:			
			rate = get_rate(Country,CurrencyFrom,CurrencyTo,(datetime.strptime(Date, '%Y-%M-%d') + timedelta(days=-1)).strftime("%Y-%M-%d"))
		else:
			rate = r.text[r.text.find('"mid":')+6:r.text.find('}]}')]		

	if Country == 'GE' and CurrencyFrom == 'GEL':
		r = requests.post('https://www.nbg.gov.ge/index.php?m=582&lng=eng', data={'item': 'ALL', 'date_start': Date, 'date_end': Date, 'x':'42', 'y':'12', 'action':'search'})
		rate = r.text[r.text.find(CurrencyTo)+3:]
		rate = rate[rate.find(CurrencyTo):]
		rate = rate[rate.find('">')+2:]
		rate = rate[rate.find('">')+2:]
		rate = rate[:rate.find('</td>')].replace(' ','').replace('\n','').strip()

	if Country == 'KZ' and CurrencyFrom == 'KZT' and CurrencyTo == 'USD':
		r = requests.post('http://www.nationalbank.kz/?docid=362&switch=english', data={'docid': '362', 'eDate': Date[-2:]+ '/' + Date[5:7] + '/' + Date[:4], 'flag': '1', 'idval': '5','OK2': 'Show report', 'sDate': Date[-2:]+ '/' + Date[5:7] + '/' + Date[:4]})
		rate = r.text[r.text.find('US DOLLAR'):]
		rate = rate[rate.find('<td align="center">')+19:]
		rate = rate[rate.find('<td align="center">')+19:]
		rate = rate[:rate.find('</td>')].replace(' ','').replace('\n','').strip()

	if Country == 'AZ' and CurrencyFrom == 'AZN':
		r = requests.get('https://www.cbar.az/currencies/' + Date[-2:]+ '.' + Date[5:7] + '.' + Date[:4] + '.xml')
		rate = r.text[r.text.find(CurrencyTo):]
		rate = rate[rate.find('<Value>')+7:rate.find('</Value>')]

	if Country == 'LT' and CurrencyFrom == 'EUR':
		r = requests.get('http://old.lb.lt/webservices/FxRates/FxRates.asmx/getFxRates', params={'tp': 'EU', 'dt': Date})
		rate = r.text[r.text.find(CurrencyTo):]
		rate = rate[rate.find('<Amt>')+5:rate.find('</Amt>')]

	if Country == 'LV' and CurrencyFrom == 'EUR':
		r = requests.get('https://www.bank.lv/vk/ecb.xml', params={'date':Date.replace('-', '')})
		rate = r.text[r.text.find(CurrencyTo):]
		rate = rate[rate.find('<Rate>')+6:rate.find('</Rate>')]

	if Country == 'EE' and CurrencyFrom == 'EUR':
		r = requests.get('https://www.eestipank.ee/en/historical-exchange-rates', params={'is_ajax':'true', 'chart_start_at':Date[-2:]+ '.' + Date[5:7] + '.' + Date[:4], 'chart_end_at':Date[-2:]+ '.' + Date[5:7] + '.' + Date[:4], 'chart_step':'day', 'currency_code': CurrencyTo})
		rate = r.text		
		if rate.find('"1 EUR = ') == -1:			
			rate = get_rate(Country,CurrencyFrom,CurrencyTo,(datetime.strptime(Date, '%Y-%M-%d') + timedelta(days=-1)).strftime("%Y-%M-%d"))
		else:
			rate = rate[rate.find('"1 EUR = ')+9:rate.find(' ' + CurrencyTo +'"}]}]')]
	
	return(rate)


print(get_rate(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]))

