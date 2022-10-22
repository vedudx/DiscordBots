# DiscordBots
## DiscordBots funtionality
- Discord Bots that I created

- if you want to reuse and edit these bots then create a database and database user on MongoDB and replace "your mongodb url" with the connection url that you create on MONGODB and replace <TOKEN> with your own discord bot token

- Ignore Firstbot.py as it is mostly my tickering bot where I test various features so it doesn't have a fixed work or features but rather a collection of discrete roles (It works though)

- StockBot.py - fetches the stock of any company listed on NASDAQ with the stock symbol. (you may not need mongoDB to locally host this bot). Look up the symbol name for the company and then <$stock companySymbol timePeriod(optional) plot(optional)>  The options for period are 1 day (1d), 5d, 1 month (1mo) , 3mo, 6mo, 1 year (1y), 2y, 5y, 10y, ytd, and max. And can alternatively use start and end instead of period where start = start date string (YYYY-MM-DD) and end = end date string (YYYY-MM-DD)
 
  commands- use $help to know more about the bot
 
          - plot command should follow $stock <companySymbol> to work, it will show a line-chart of specified company's stock open price with respect to date.
 
          - $name <companySymbol> fetches the Fullname of the company
 
          - eg $stock AAPL 1y plot will fetch the first three days and last three days of the specified time part in a table and the plot as well
 
          - eg $stock AAPL will fetch the first three days and last three days of the specified time part(default is whole time- meaning first three days after the listing of stock and present three days) in a table
