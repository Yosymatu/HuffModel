from huffcalculate import Calculate
import json
import numpy as np
import pandas as pd

calculate = Calculate()


#データのロード
with open('100_pop.geojson', 'r', encoding="utf-8") as f:
    pop = json.load(f)

with open('AB_com.geojson', 'r', encoding="utf-8") as f:
    com = json.load(f)

#100mメッシュの点を取得
pop_ptList = [i['geometry']['coordinates'] for i in pop['features']]
#商業施設座標の取得
com_ptList = [i['geometry']['coordinates'] for i in com['features']]
#売場面積の取得
com_areaList = [i['properties']['売場面積'] for i in com['features']]

#出力用に取得
#meshcodeの取得
pop_meshcodeList = [i['properties']['MESHCODE'] for i in pop['features']]
#keycodeの取得
pop_keycodeList = [i['properties']['KEYCODE'] for i in pop['features']]


allPij = []
for j in range(len(pop_ptList)):
    disj = [calculate.Dist(pop_ptList[j], i, True) for i in com_ptList]
    Pij = calculate.oneAttract(disj, com_areaList, 1, 2)
    Pij.insert(0, pop_meshcodeList[j])
    Pij.insert(1, pop_keycodeList[j])
    allPij.append(Pij)

allPij = pd.DataFrame(allPij)
allPij.to_csv('Huff.csv')
