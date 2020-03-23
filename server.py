from flask import Flask
import er

app = Flask(__name__)

@app.route('/<Country>/<CurrencyFrom>/<CurrencyTo>/<Date>/')
def hello(Country,CurrencyFrom,CurrencyTo,Date):
	return er.get_rate(Country,CurrencyFrom,CurrencyTo,Date)

if __name__ == "__main__":
	app.run()
