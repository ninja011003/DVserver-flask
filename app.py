from flask import Flask,request,send_file,jsonify,render_template_string
from datetime import datetime, timedelta
from io import BytesIO
import requests
import matplotlib.pyplot as plt
import base64

app = Flask(__name__)

def unix_timestamp_to_yyyy_mm_dd(unix_timestamp):
    # Convert the Unix timestamp to a Python datetime object
    dt_object = datetime.fromtimestamp(unix_timestamp)
    
    # Format the datetime object as 'yyyy-mm-dd'
    formatted_date = dt_object.strftime('%Y-%m-%d')
    
    return formatted_date

@app.route('/',methods=['GET'])
def handle():
    return 'dv vizualization server'
#HC0XU4M8A1I6N6BU
#22SWW3DF4I4QDAWY
@app.route('/getStockGraph', methods=['GET'])
def handle_get_request():
    stock_name = request.args.get('stockName')
    url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords='+stock_name+'&apikey=HC0XU4M8A1I6N6BU'
    r = requests.get(url)
    data = r.json()
    #print(data['bestMatches'][0]['1. symbol'])
    #print(data)
    stock_symbol =data['bestMatches'][0]['1. symbol']
    
    # Get today's date
    today = datetime.now().date()
    # Get the same date one month ago
    one_month_ago = (datetime.now() - timedelta(days=30)).date()
    url = "https://yfinance-stock-market-data.p.rapidapi.com/price-customdate"
    
    payload = {
        "symbol": stock_symbol,
        "end": today,
        "start": one_month_ago
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "2179808fd1msh04d9b9f1e7bdb1ep16ca8cjsn758d66e63226",
        "X-RapidAPI-Host": "yfinance-stock-market-data.p.rapidapi.com"
    }

    response = requests.post(url, data=payload, headers=headers)
    data= response.json();
    dates=[]
    prices=[]
    for daton in data['data']:
        dates.append(unix_timestamp_to_yyyy_mm_dd(int(daton['Date'])/1000))
        prices.append(daton['Adj Close'])
    # Create the line chart
    plt.figure(figsize=(10, 8))
    plt.plot(dates,prices, marker='o', linestyle='-')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Price Line Chart')
    plt.grid(True)
    plt.xticks(rotation=45)
    
    # Save the chart as an image
    # plt.savefig('line_chart.png')
    
     # Save the chart in memory buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Clear the current figure to release resources
    plt.clf()

    return send_file(buffer, mimetype='image/png')

    #return render_template_string(html_template, chart_data=encoded_image)

if __name__ == '__main__':
    app.run(debug=True,port =6969)
