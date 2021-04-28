API_KEY = 'pk_c1049f390fb443b9b0a74dad009c9827'

# "Quote" endpoint example
#https://cloud.iexapis.com/stable/stock/AAPL/quote/latestPrice?token=pk_c1049f390fb443b9b0a74dad009c9827
API_DATA_URL= "https://cloud.iexapis.com/stable/stock/{}/quote?token=" + API_KEY


testsymbol = 'csco'
# "Key Stats" endpoint example
#https://cloud.iexapis.com/stable/stock/aapl/stats?token=pk_c1049f390fb443b9b0a74dad009c9827
DIVIDEND_URL = "https://cloud.iexapis.com/stable/stock/"+testsymbol+"/stats?token=" + API_KEY