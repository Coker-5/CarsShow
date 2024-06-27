import csv
import os

import requests
from lxml import etree


class spider(object):
    def __init__(self):
        self.url = "https://www.dongchedi.com/motor/pc/car/rank_data"
        self.params = {
            "aid": "1839",
            "app_name": "auto_web_pc",
            "city_name": "长沙",
            "count": "10",
            "offset": "10",
            "month": "",
            "new_energy_type": "",
            "rank_data_type": "11",
            "brand_id": "",
            "price": "",
            "manufacturer": "",
            "outter_detail_type": "",
            "nation": "0"
        }
        self.headers = {
            "referer": "https://www.dongchedi.com/sales/city-x-x-x-x",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        }

    def init(self):
        if not os.path.exists("./temp.csv"):
            with open("./data.csv", "a", newline="", encoding="utf-8") as fp:
                write = csv.writer(fp)
                write.writerow(
                    ["brand", "carName", "saleVolume", "price", "manufacturer", "rank", "carModel", "energyType",
                     "marketTime", "insure"])

    def main(self):
        count = 0
        for i in range(0, 45):
            self.params['offset'] = i
            pageJson = requests.get(url=self.url, params=self.params, headers=self.headers).json()
            pageJson = pageJson['data']['list']
            for index, car in enumerate(pageJson):
                try:
                    carData = []
                    count = count + 1
                    print(f"正在爬取第{count}条数据")
                    carData.append(car["brand_name"])
                    carData.append(car["series_name"])
                    carData.append(car["count"])
                    price = []
                    price.append(car["min_price"])
                    price.append(car["max_price"])
                    carData.append(price)
                    carData.append(car["sub_brand_name"])
                    carData.append(car["rank"])
                    carId = car["series_id"]

                    infoHTML = requests.get(url="https://www.dongchedi.com/auto/params-carIds-x-%s" % carId,
                                            headers=self.headers)
                    infoHTMLpath = etree.HTML(infoHTML.text)
                    # carModel
                    carModel = infoHTMLpath.xpath("//div[@data-row-anchor='jb']/div[2]/div/text()")[0]
                    carData.append(carModel)
                    # energyType
                    energyType = infoHTMLpath.xpath("//div[@data-row-anchor='fuel_form']/div[2]/div/text()")[0]
                    carData.append(energyType)
                    # maketTime
                    marketTime = infoHTMLpath.xpath("//div[@data-row-anchor='market_time']/div[2]/div/text()")[0]
                    carData.append(marketTime)
                    # insure
                    insure = infoHTMLpath.xpath("//div[@data-row-anchor='period']/div[2]/div/text()")[0]
                    carData.append(insure)
                    print(carData)
                    self.save_to_csv(carData)
                except Exception as e:
                    print(e)

    def save_to_csv(self, resultData):
        with open("data.csv", "a", newline="", encoding="utf-8") as fp:
            writer = csv.writer(fp)
            writer.writerow(resultData)


if __name__ == '__main__':
    spiderObj = spider()
    spiderObj.init()
    spiderObj.main()
