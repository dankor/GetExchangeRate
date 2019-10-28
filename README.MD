A simple script to parse xml, json, html, etc in order to get the value of exchange rate from specific central bank. Depends on the "requests" module.

### How it works:

```
python er.py 'KZ' 'KZT' 'USD' '2018-05-01'
```

Have to return:

```
327.25
```

Where:
* 'KZ' — Country code
* 'KZT' — Input currency code
* 'USD' — Output currency code
* '2018-05-01' — Date of the rate

### Supports list

#### Country code

* EE
* UA
* BY
* KZ
* LT
* PL
* LV
* AZ
* RU
* GE
* UZ

#### Input currency code

* AZN
* RUB
* KZT
* GEL
* PLN
* EUR
* UAH
* BYN
* UZS

#### Output currency code

Any. Depends on central bank, except KZ (it's USD only so far).

