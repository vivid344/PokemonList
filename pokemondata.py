# ファイル操作
import glob
import csv
import re
import linecache

# データ処理・視覚化
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

# クローラー
import time
from datetime import datetime
from bs4 import BeautifulSoup
import requests


def GetPokemonData():
    f = open('pokemon.csv', 'w')
    mainurl = "https://ja.wikipedia.org/wiki/ポケモン一覧"
    response = requests.get(mainurl)
    response.encoding = 'UTF-8'

    link = BeautifulSoup(response.content, "lxml")

    pokemonurl = link.findAll("li")

    list = []

    for pokemon in pokemonurl:
        pokemondata = pokemon.find("a",title=re.compile("^ポケモンの一覧"))
        try:
            pokemonurl = pokemondata.get('href')
        except:
            continue

        pokemonurl = "https://ja.wikipedia.org" + str(pokemonurl)
        responsedata = requests.get(pokemonurl)
        responsedata.encoding = 'UTF-8'
        linkpokemon = BeautifulSoup(responsedata.content, "lxml")

        pokemondetail = linkpokemon.findAll("span",{"mw-headline"})

        for number in range(1,len(pokemondetail)-1):
            if pokemondetail[number].string == "脚注":
                break
            if pokemondetail[number].string == "注釈":
                break

            print(pokemondetail[number].string)
            list = [
                pokemondetail[number].string
            ]
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(list)

    f.close()

def merge():
    list = []
    f = open('pokemondata.csv', 'w')
    f1 = open('pokemon.csv', 'r')
    pokemonnumber = 1
    reader = csv.reader(f1)
    for row in reader:
        if row not in list:
            list.append(row)
    for line in list:
        writer = csv.writer(f, lineterminator='\n')
        line = re.sub('\[|\]|\'', "", str(line))
        writer.writerow(["No."+str(pokemonnumber),line])
        pokemonnumber = pokemonnumber + 1

    f.close()

def check():
    print("もう一度検索しますか？ yes or no.")
    test2 = str(input('> '))
    if test2 == "yes":
        print("\n")
        DispPokemon()
    elif test2 == "no":
        print("\n")
        pass
    else:
        print("正しい値を入力してください")
        print("\n")
        check()

def DispPokemon():
    count = 0
    f = open('pokemondata.csv', 'r')
    print("図鑑番号を入力してください（No1〜802まで）")
    test = int(input('> '))

    if 1<=test<=802:
        print(re.sub(',','　',linecache.getline("pokemondata.csv", int(test))))
    else:
        print("正しい値を入力してください\n")
        count = 1

    if count == 1:
        DispPokemon()
    else:
        check()

GetPokemonData()
#merge()
#DispPokemon()