import os, time
import discord
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

TOKEN = 'YOUR_TOKEN'

client = discord.Client()

def findLowestPriceFor(listOfGraficscards):

    print("fetching data")
    answer = ""

    options = Options()
    options.add_argument("--headless")
    web = webdriver.Chrome("chromedriver.exe", options=options)

    web.get("https://geizhals.de/")
    time.sleep(1)
    web.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
    time.sleep(1)
    web.find_element_by_xpath('//*[@id="mkat"]/li[1]').click()
    time.sleep(1)
    web.find_element_by_partial_link_text("Grafikkarten").click()
    time.sleep(1)
    web.find_element_by_partial_link_text("PCIe").click()
    time.sleep(1)
    web.find_element_by_xpath('//*[@id="steel_list_container lazy-list--categorylist"]/div[1]/div[6]/a').click()

    for gc in listOfGraficscards:
        try:
            web.find_element_by_partial_link_text(gc).click()
            price = web.find_element_by_xpath('//*[@id="product0"]/div[6]/span/span').text
            web.find_element_by_partial_link_text(gc).click()
        except:
            price = "No info"
        finally:
            time.sleep(1)
            answer += gc + ": " + price.replace("+", " ") + "\n"

    return answer



@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.content.startswith("info"):
        if message.content == 'info help':

            response = discord.Embed(title="Help:", description="info rtx: rtx prices\ninfo gtx: gtx prices", color=discord.colour.Colour.random())

            await message.channel.send(embed=response)

        elif message.content == 'info rtx':

            rtx = ["RTX 2080 Ti", "RTX 3060 Ti", "RTX 3070", "RTX 3080", "RTX 3090"]
            await message.channel.send("*fetching data*")

            try:
                response = discord.Embed(title="RTX prices:", url="https://geizhals.de/?cat=gra16_512", description=findLowestPriceFor(rtx), color=discord.colour.Colour.random())
                await message.channel.send(embed=response)
            except:
                await message.channel.send("An unexpected error occured")

        elif message.content == "info gtx":

            gtx = ["GTX 1660 Ti", "GTX 1660 SUPER", "GTX 1660", "GTX 1650 SUPER", "GTX 1650", "GTX 1060", "GTX 1050 Ti"]

            await message.channel.send("*fetching data*")

            try:
                response = discord.Embed(title="RTX prices:", url="https://geizhals.de/?cat=gra16_512", description=findLowestPriceFor(gtx), color=discord.colour.Colour.random())
                await message.channel.send(embed=response)
            except:
                await message.channel.send("An unexpected error occured")
        else:
            await message.channel.send("This is no valid info command")
client.run(TOKEN)