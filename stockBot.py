import yfinance as yf
import discord
import pandas as pd
import os
import requests
import json
import random
from discord.ext import commands
#import pymongo
#from pymongo import MongoClient


#improve the code and add functionality for time, and better help instructions
def get_name(message):
    company=yf.Ticker(message[1])
    return company.info['shortName']
#returns the country 
def get_country(message):
    company=yf.Ticker(message[1])
    return company.info['country']
#returns the stock 
def get_stock(message):
    message_list = message.split()
    company = yf.Ticker(message_list[1])
    
    if len(message_list) >= 4 and message_list[3] != 'plot':
        startDate = message_list[2]
        endDate = message_list[3]
        share_price=company.history(start=startDate, end = endDate)
        
    elif len(message_list) >= 3 and message_list[2] != 'plot':
        time = message_list[2]
        share_price = company.history(period=time)
    else:
        share_price = company.history(period = "max")

    share_price = share_price.round(decimals=3)
    if 'plot' in message_list:
        plot = share_price.plot(y = 'Open', title = company.info['shortName'])
        fig = plot.get_figure()
        name = message_list[1]
        fig.savefig(name+".png")
        

    return str(share_price.head(3).append(share_price.tail(3)))


client = discord.Client()

#when discord bot is active
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    message_list = message.content.split()
    if message.author == client.user:
        return
    
    #if user message while summoning chooses 'help', it displays the options available
    if message.content.startswith('$help'):
        url = 'https://stocks.tradingcharts.com/stocks/symbols/s'
        msg = 'look up the symbol name for the company and then <$stock companySymbol timePeriod>' + "  The options for period are 1 day (1d), 5d, 1 month (1mo) , 3mo, 6mo, 1 year (1y), 2y, 5y, 10y, ytd, and max. And can alternatively use start and end instead of period where start = start date string (YYYY-MM-DD) and end = end date string (YYYY-MM-DD)"
        await message.channel.send(msg+url)
    
    #if user message while summoning bot starts with stock
    if message.content.startswith('$stock'): #have to add a specific author option
        await message.channel.send('data of first three and last three days of the asked time period')
        stock = get_stock(message.content)
        stock_msg = '```'+stock+'```'
        await message.channel.send(stock_msg)
       
        #if user message contains both stock and plot
        if 'plot' in message.content:
            img_name = message_list[1]+".png"
            with open(img_name, 'rb') as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)

    # if user message while summoning bot starts with country
    elif message.content.startswith('$country'):
        count = get_country(message_list)
        await message.channel.send(count)

    elif message.content.startswith('$name'):
        name = get_name(message_list)
        await message.channel.send(name)

#token = ODUyMDcwMDA3OTQ4OTY3OTY2.YMBeCA.YFDKv6qnfzYcWuo9K7a0FLrjcjg


client.run('ODUyMDcwMDA3OTQ4OTY3OTY2.YMBeCA.lAQXbz4lTGAw7_fBkagrJ72f1hw')
