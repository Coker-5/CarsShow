import csv
import random


class SourceDataDemo:

    def __init__(self):
        self.origin_data=[]
        self.table_data = self.load_csv()
        self.mySaleCount=self.saleCount()
        self.energyCount=self.energyType()
        self.carModel()
        self.carPrice()
        self.brand,self.ele_count,self.gaso_count,self.mix_count=self.energyProp()
        self.price_statics=self.carPrice()
        self.counter = {'name': '车辆销售今日之最', 'value': self.table_data[0]["brand"]}
        self.counter2 = {'name': '车辆最高销售额', 'value': self.table_data[0]["saleVolume"]}
        self.saleVolume=[{'name': i['carName'], 'value': i['saleVolume']} for i in self.table_data[:6]]
        brand_name=[i['name'] for i in self.energyCount[1]]
        random.shuffle(self.saleVolume)
        self.echart1_data = {
            'title': '汽车车型销量排行',
            'data': self.saleVolume
        }
        self.echart2_data = {
            'title': '汽车品牌总销排行',
            'data': self.mySaleCount
        }
        self.echarts3_1_data = {
            'title': '油车占比',
            'data': self.energyCount[0]
        }
        self.echarts3_2_data = {
            'title': '电车占比',
            'data': self.energyCount[1]
        }
        self.echarts3_3_data = {
            'title': '混动占比',
            'data': self.energyCount[2]
        }
        self.echart4_data = {
            'title': '动力类型',
            'data': [
                {"name": "纯电动", "value": self.ele_count},
                {"name": "汽油", "value": self.gaso_count}
            ],
            'xAxis': self.brand,
        }
        self.echart5_data = {
            'title': '车型规模占比',
            'data': self.carModel()
        }
        self.echart6_data = {
            'title': '汽车售价占比',
            'data': [
                {"name": "0-5w", "value": self.price_statics["0-5w"], "value2": 20, "color": "01", "radius": ['59%', '70%']},
                {"name": "5-10w", "value": self.price_statics["5-10w"], "value2": 30, "color": "02", "radius": ['49%', '60%']},
                {"name": "10-20w", "value": self.price_statics["10-20w"], "value2": 35, "color": "03", "radius": ['39%', '50%']},
                {"name": "20-30w", "value": self.price_statics["20-30w"], "value2": 40, "color": "04", "radius": ['29%', '40%']},
                {"name": "30w以上", "value": self.price_statics["30w以上"], "value2": 50, "color": "05", "radius": ['20%', '30%']},
            ]
        }
        self.map_1_data = {
            'symbolSize': 100,
            'data': [
                {'name': '海门', 'value': 239},
                {'name': '鄂尔多斯', 'value': 231},
                {'name': '招远', 'value': 203},
            ]
        }

    def load_csv(self):
        data = []
        with open("./spider/data.csv", "r", encoding="utf-8") as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                data.append(row)
        return data


    def saleCount(self):
        brand_sales = {}

        for car in self.table_data:
            brand = car['brand']
            sale_volume = int(car['saleVolume'])

            if brand in brand_sales:
                brand_sales[brand] += sale_volume
            else:
                brand_sales[brand] = sale_volume

        sales_items=[]
        for k,v in brand_sales.items():
            sales_items.append({'name':k,'value':v})
        return sales_items[:8]

    def energyType(self):
        # 初始化字典用于统计每个品牌的车辆数量
        electric_count = {}
        gasoline_count = {}
        mix_count={}
        energy_data=[]

        # 遍历每辆车的信息
        for car in self.table_data:
            if car['energyType'] == '纯电动':
                brand = car['brand']
                if brand in electric_count:
                    electric_count[brand] += 1
                else:
                    electric_count[brand] = 1
            elif car['energyType'] == '汽油':
                brand = car['brand']
                if brand in gasoline_count:
                    gasoline_count[brand] += 1
                else:
                    gasoline_count[brand] = 1
            elif car['energyType'] == '插电式混合动力':
                brand = car['brand']
                if brand in mix_count:
                    mix_count[brand] += 1
                else:
                    mix_count[brand] = 1
        self.origin_data.append(electric_count)
        self.origin_data.append(gasoline_count)
        self.origin_data.append(mix_count)

        electric_count=[{"name":k,"value":v} for k,v in electric_count.items()]
        gasoline_count=[{"name":k,"value":v} for k,v in gasoline_count.items()]
        mix_count=[{"name":k,"value":v} for k,v in mix_count.items()]
        energy_data.append(electric_count)
        energy_data.append(gasoline_count)
        energy_data.append(mix_count)

        return energy_data


    def energyProp(self):
        car_brands = []
        ele_count=[]
        gaso_count=[]
        mix_count=[]

        for sublist in self.energyCount:
            for item in sublist:
                car_brands.append(item['name'])

        car_brands=list(set(car_brands))

        # 统计每个品牌的车数量，不存在的品牌补0
        for brand in car_brands:
            if brand in self.origin_data[0]:
                ele_count.append(self.origin_data[0][brand])
            else:
                ele_count.append(0)

        for brand in car_brands:
            if brand in self.origin_data[1]:
                gaso_count.append(self.origin_data[1][brand])
            else:
                gaso_count.append(0)

        for brand in car_brands:
            if brand in self.origin_data[2]:
                mix_count.append(self.origin_data[2][brand])
            else:
                mix_count.append(0)

        return car_brands,ele_count,gaso_count,mix_count

    def carModel(self):
        model_count = {}

        for car in self.table_data:
            car_model = car['carModel']
            if car_model in model_count:
                model_count[car_model] += 1
            else:
                model_count[car_model] = 1

        carModel_count = [{"name": k, "value": v} for k, v in model_count.items()][:6]
        return carModel_count

    def carPrice(self):
        prices_first_values = []
        price_statics={"0-5w":0,"5-10w":0,"10-20w":0,"20-30w":0,"30w以上":0}

        for car in self.table_data:
            price_str = car['price']
            price_list = eval(price_str)
            first_value = price_list[0]
            prices_first_values.append(first_value)

        for i in prices_first_values:
            if i<=5:
                price_statics["0-5w"]+=1
            elif i<=10:
                price_statics["5-10w"]+=1
            elif i<=20:
                price_statics["10-20w"]+=1
            elif i<=30:
                price_statics["20-30w"]+=1
            elif i>30:
                price_statics["30w以上"]+=1

        return price_statics


    @property
    def echart1(self):
        data = self.echart1_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'series': [i.get("value") for i in data.get('data')]
        }
        return echart

    @property
    def echart2(self):
        data = self.echart2_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'series': [i.get("value") for i in data.get('data')]
        }
        return echart

    @property
    def echarts3_1(self):
        data = self.echarts3_1_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'data': data.get('data'),
        }
        return echart

    @property
    def echarts3_2(self):
        data = self.echarts3_2_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'data': data.get('data'),
        }
        return echart

    @property
    def echarts3_3(self):
        data = self.echarts3_3_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'data': data.get('data'),
        }
        return echart

    @property
    def echart4(self):
        data = self.echart4_data
        echart = {
            'title': data.get('title'),
            'names': [i.get("name") for i in data.get('data')],
            'xAxis': data.get('xAxis'),
            'data': data.get('data'),
        }
        return echart

    @property
    def echart5(self):
        data = self.echart5_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'series': [i.get("value") for i in data.get('data')],
            'data': data.get('data'),
        }
        return echart

    @property
    def echart6(self):
        data = self.echart6_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'data': data.get('data'),
        }
        return echart

    @property
    def map_1(self):
        data = self.map_1_data
        echart = {
            'symbolSize': data.get('symbolSize'),
            'data': data.get('data'),
        }
        return echart


class SourceData(SourceDataDemo):

    def __init__(self):
        super().__init__()
        self.title = '全国汽车大数据可视化平台'