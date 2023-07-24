"""
Mini project on Stock Performance Analysis of major MNCs(Apple, Google, Microsoft and Netflix)
The data(3 months from now) is being imported using yfinance(yahoo finance) module directly from the internet
The data is analyzed, visualized using appropriate graphs using plotly module
"""
import yfinance
import pandas
from datetime import datetime
import plotly.express

#Specifying the start and end dates of the data
start_date = datetime.now() - pandas.DateOffset(months=3)
end_date = datetime.now()

#selecting the stocks(Stocks of few MNCs are being taken)
Company = {"Microsoft":"MSFT" , "Netflix":"NFLX" , "Google":"GOOGL" , "Apple":"AAPL"}

#Creating a list data by downloading the Stocks data from the internet usng yfinance
dataframe_list = []
for company in Company.values():
    data = yfinance.download(company,
                             start = start_date,
                             end =end_date)
    dataframe_list.append(data)

#Creating and printing a dataframe with Ticker name and Date
dataframe= pandas.concat(dataframe_list,
                         keys= Company,
                         names=['Company','Date'])
print(dataframe.head())
print(dataframe.tail())

#Resetting the index of the data list
dataframe = dataframe.reset_index()
print(dataframe.head())
print(dataframe.tail())

#Plotting a line graph of stocks performance data
fig_1 = plotly.express.line(dataframe,
                            x="Date",
                            y="Close",
                            color = "Company",
                            labels={"Close" : "Closing value"},
                            title = "Stocks Performance <last 3 months> : ")
fig_1.show()

#Plotting an area graph of stocks performance data
fig_2 = plotly.express.area(dataframe,
                            x='Date',
                            y='Close',
                            color = 'Company',
                            facet_col = "Company",
                            labels = {'Date':"Date range",
                                "Close" : "Closing value"},
                            title = "Stock Prices")
fig_2.show()

#Calculating the moving average with grouping sizes(10,20)
dataframe['Moving_Average_10'] = dataframe.groupby('Company')['Close'].rolling(window=10).mean().reset_index(0, drop=True)
dataframe['Moving_Average_20'] = dataframe.groupby('Company')['Close'].rolling(window=20).mean().reset_index(0, drop=True)

#Printing moving averages of all stocks(group size 10, 20)
for company, group in dataframe.groupby('Company'):
    print(f"Moving Average for {company}:")
    print(group[['Moving_Average_10','Moving_Average_20']])

#Plotting line graphs for moving averages of all stocks(group size 10, 20)
for company, group in dataframe.groupby('Company'):
    fig_3 = plotly.express.line(group,
                                x='Date',
                                y=['Close', 'Moving_Average_10', 'Moving_Average_20'],
                                title=f"Moving averages of {company} stocks: ")
    fig_3.show()

#Analyzing volatility of all stocks and plotting combined line graph
dataframe['Volatility'] = dataframe.groupby('Company')['Close'].pct_change().rolling(window=10).std().reset_index(0, drop=True)
fig_4 = plotly.express.line(dataframe,
                            x= "Date",
                            y="Volatility",
                            color ="Company",
                            title="Stocks volatility")
fig_4.show()

#Calculating and plotting scatter chart of the correlation between stocks of Apple and Microsoft
apple = dataframe.loc[dataframe['Company']== 'Apple',['Date', 'Close']].rename(columns={'Close':'Apple'})
microsoft = dataframe.loc[dataframe['Company']== 'Microsoft',['Date', 'Close']].rename(columns={'Close':'Microsoft'})
dataframe_correlation = pandas.merge(apple,microsoft, on='Date')
fig_5 = plotly.express.scatter(dataframe_correlation,
                               x='Apple',
                               y='Microsoft',
                               trendline='expanding',
                               title='Co-relation <expanding> between Apple and Microsoft')
fig_5.show()

#Calculation of cumulative returns and plotting it using area graph
#Here, we are creating a column Daily returns using percentage change(in lambda function)
dataframe['Daily_Return'] = dataframe.groupby('Company')['Close'].transform(lambda x: x.pct_change())
print(dataframe)
#We calculate the cumulative returns using cumulative sum (cumsum())
dataframe['Cumulative_Return'] = (1 + dataframe.groupby('Company')['Daily_Return'].cumsum()).reset_index(0, drop=True)
#Plotting the cumulative returns using area graph ranging 0.95 to 1.4
fig_6 = plotly.express.area(dataframe,
                            x='Date',
                            y='Cumulative_Return',
                            color='Company',
                            facet_col='Company',
                            facet_col_wrap=2 ,
                            labels={'Cumulative_Return':'Cumulative returns'},
                            title='Cumulative returns of stocks: ',
                            range_y=[0.95,1.4])
fig_6.show()

#Sentiment analysis(simple approach)
def get_sentiment_score(text):
    # Here, you can implement a basic sentiment analysis logic to determine positive, negative, or neutral sentiment
    # For simplicity, let's assume positive sentiment if the stock price increased, negative if it decreased, and neutral otherwise
    if text > 0:
        return "Positive"
    elif text < 0:
        return "Negative"
    else:
        return "Neutral"
#Calculate sentiment for each company stocks
dataframe['Sentiment'] = dataframe.groupby('Company')['Close'].pct_change().apply(get_sentiment_score)
print(dataframe)
# Plot the sentiment analysis
fig_7 = plotly.express.line(dataframe.reset_index(), x='Date', y='Close', color='Sentiment', title='Market sentiment analysis')
fig_7.show()

#Analyze the trading volume of each stock and visualize it using a bar graph
fig_8 = plotly.express.bar(dataframe,
                           x='Date',
                           y='Volume',
                           color='Company',
                           title='Trading volume of stocks: ')
fig_8.show()
