import numpy as np

#計算クラス群
class Calculate:
    
    #距離を測定
    def Dist(self, p1, p2, mode):
        '''
        二地点間の距離を求めるメソッド
        ヒュベニの公式から距離を求める（国土地理院でも同様な方法）

        @param p1,p2 緯度経度（度）をリストで持つもの
        @param mode 測地系 true:世界 false:日本
        @return float 距離(m)
        '''

        #度→ラジアンに変更
        radLat1 = np.deg2rad(p1[0])
        radLon1 = np.deg2rad(p1[1])
        radLat2 = np.deg2rad(p2[0])
        radLon2 = np.deg2rad(p2[1])

        #緯度経度差
        radLatDiff = radLat1 - radLat2
        radLonDiff = radLon1 - radLon2

        #平均経度
        radLatAve = (radLat1 + radLat2) / 2

        #測地系の違い
        if mode == True:
            a = 6378137.0
            b = 6356752.314140356
        else:
            a = 6377397.155
            b = 6356078.963

        #第一離心率^2
        e2 = (a*a - b*b) / (a*a)
        #赤道上の子午線曲率半径
        a1e2 = a * (1 - e2)

        sinLat = np.sin(radLatAve)
        W2 = 1.0 - e2 * (sinLat*sinLat)
        #子午線曲率半径M
        M = a1e2 / (np.sqrt(W2)*W2)
        #卯酉線曲率半径
        N = a / np.sqrt(W2)

        t1 = M * radLatDiff
        t2 = N * np.cos(radLatAve) * radLonDiff
        dist = np.sqrt((t1*t1) + (t2*t2))

        return dist

    def oneAttract(self, distList, areaList, alpha, beta):
        '''
        顧客が店舗(dist, area)での確率を求めるメソッド
        参照 http://desktop.arcgis.com/ja/arcmap/10.3/tools/business-analyst-toolbox/how-original-huff-model-works.htm

        @apram distList すべての店舗までの距離のリスト
        @param areaList すべての店舗の売場面積のリスト
        @param alpha 距離修正係数
        @param beta 売場面積修正係数
        @return 店舗の魅力度のリスト
        '''
        #すべての店舗の魅力度を計算
        WList = [np.power(iarea, beta)/np.power(idist, alpha) for idist, iarea in zip(distList, areaList)]
        #すべての店舗へ行く確率を計算
        PList = [iW/sum(WList) for iW in WList]

        return PList

# if __name__ == '__main__':
#     calcualte = Calculate()