import datetime
import plot
import geo_plot
from st_chart import stChart
import port_distribution
import pandas as pd
import numpy as np


class stAPI:
    """
    API主要功能：传入源数据后进行数据预处理、输出画图所需格式的数据
    @:param st_df 春运源数据(Dataframe)
    @:param all_df 地理数据(Dataframe)
    @:param departure_port 方便函数处理，减少重复代码
    @:param destination_port 方便函数处理，减少重复代码

    """
    def __init__(self, st_df, all_df):
        self.st_df = st_df
        self.all_df = all_df
        self.p_p_c_dict = {}

        # apply, 调用上面的函数，指定列下的每个数据都要过一次
        self.st_df['出发站'] = self.st_df['出发站'].apply(self._normalization)
        self.st_df['到达站'] = self.st_df['到达站'].apply(self._normalization)

        self._if_booking()
        self._judge_train_type()

        self.departure_port = self.st_df['出发站']
        self.destination_port = self.st_df['到达站']

        self.departure_port = self.departure_port.drop_duplicates()
        self.departure_port = self.departure_port.tolist()

        self.destination_port = self.destination_port.drop_duplicates()
        self.destination_port = self.destination_port.tolist()

        self._pre_process()

    # 标准化 把’贵  阳北‘ 改成 ’贵阳北‘
    def _normalization(self, x):
        x = x.replace(' ', '')
        return x

    def _judge_train_type(self):
        hsr_type = []

        # 高铁命名规则：G代表高，D代表动车，K代表快车，这里只需要区分高铁和其他列车类型所以1为高铁0为其他
        def if_g(x):
            if str(x)[0] == 'G':
                hsr_type.append(1)

            else:
                hsr_type.append(0)

        self.st_df['车次'].apply(if_g)
        self.st_df['rail_type'] = hsr_type

    def _if_booking(self):
        # 是否可预约，实现方式同上
        if_booking = []

        def if_b(x):
            if str(x) == '预订':
                if_booking.append(1)

            else:
                if_booking.append(0)

        self.st_df['可以预定'].apply(if_b)
        self.st_df['if_booking'] = if_booking

    def _detection_port(self, port):
        need_change = []
        not_exist_port = []
        for i in port:
            f = i.replace(' ', '')
            if f not in self.all_df['站名'].unique():
                # print(i)
                index = port.index(i)
                port[index] = port[index].replace(' ', '') + "站"
                need_change.append(port[index])

                if port[index] not in self.all_df['站名'].unique():
                    # print(port[index])
                    not_exist_port.append(need_change[need_change.index(port[index])])
                    del need_change[need_change.index(port[index])]

        return need_change, not_exist_port

    # 预处理好数据
    def _pre_process(self):
        d1_change, not_1 = self._detection_port(self.departure_port)
        d2_change, not_2 = self._detection_port(self.destination_port)

        def change(x):
            # 如果元素+站在列表中，则返回元素+站，即保证春运数据与地理数据相同
            if x + '站' in d1_change:
                return x + '站'

            else:
                return x

        def change_2(x):
            if x + '站' in d2_change:
                return x + '站'

            else:
                return x

        self.st_df['出发站'] = self.st_df['出发站'].apply(change)
        self.st_df['到达站'] = self.st_df['到达站'].apply(change_2)

        # 根据not_1 not_2 找到脏数据的索引
        lose_count = []
        for i in not_1:
            lose_index_1 = self.st_df[(self.st_df['出发站'] == i[:-1])].index.tolist()
            lose_count.extend(lose_index_1)

        for i in not_2:
            lose_index_1 = self.st_df[(self.st_df['到达站'] == i[:-1])].index.tolist()
            lose_count.extend(lose_index_1)

        # 删除站点不匹配数据
        self.st_df.drop(lose_count, inplace=True)
        self.st_df.index = range(0, 411241)

        # 任务5
        # 将两个series转化为列表
        dep_p = self.st_df['出发站'].tolist()
        des_p = self.st_df['到达站'].tolist()
        # 直辖市
        municipalities = ['天津', '北京', '上海', '重庆']
        # 只提取三个字段
        p_p_c = self.all_df[['站名', '省', '市']]

        # Method 3 use 0.04999971389770508 seconds
        # 去重
        p_p_c = p_p_c.drop_duplicates()
        # 创建一个字典内嵌字典即{'': {'': ''}} 提高查询速度

        for i in range(p_p_c.shape[0]):
            self.p_p_c_dict[p_p_c.iloc[i, :]['站名']] = {'省': p_p_c.iloc[i, :]['省'], '市': p_p_c.iloc[i, :]['市']}

        '''
            @:param port: 出发站或到达站的站名
            功能： 提取站点所在城市
            主要思路： 如果当前站点的省份是在直辖市中，那么应该将省字段下的数据传入city中，否则将市字段下的传入city
        '''

        def filter_city(port):
            city = []
            for i in port:
                if self.p_p_c_dict[i]['省'] in municipalities:
                    city.append(self.p_p_c_dict[i]['省'])

                else:
                    city.append(self.p_p_c_dict[i]['市'])

            return city

        # 调用函数
        city1 = filter_city(des_p)
        city2 = filter_city(dep_p)

        # 加入city列
        self.st_df['dep_city'] = city2
        self.st_df['des_city'] = city1

        dep_to_dest = []

        # 将出发城市和到达城市建立联系， 形式如 "上海-长春"
        for i, j in zip(city2, city1):
            dep_to_dest.append("{}-{}".format(i, j))

        # 增添字段
        self.st_df['dep_to_dest'] = dep_to_dest

        # 清洗脏数据
        a = self.st_df[(self.st_df['出发时间'] == '-----')].index.tolist()
        self.st_df = self.st_df.drop(a)

        # 清洗脏数据， 数据本身有问题
        def find_error(x):
            if len(x) == 2:
                return "0:15"

            if len(x) == 3:
                l = list(x)
                l.insert(1, ':')
                l = ''.join(l)
                return l

            if len(x) == 4 and ':' not in x:
                l = list(x)
                l.insert(2, ':')
                l = ''.join(l)
                return l

            return x

        self.st_df['出发时间'] = self.st_df['出发时间'].apply(find_error)

        # high_speed_rail_info['出发时间'] = pd.to_datetime(high_speed_rail_info['出发时间'], format="%H:%M")

        # string转化为datetime，用于比较时间从而划分时间段
        def to_datetime(x):
            t = datetime.datetime.strptime(x, "%H:%M").time()

            return t

        self.st_df['出发时间'] = self.st_df['出发时间'].apply(to_datetime)

    '''
        @:param dep_time: 出发时间 划分为四个时间段
        @:param search_time: 查询时间，即共四天
        @:return rails: 即当前所选时间段和查询时间的列车调度情况
        @:return rail_group: 即当前所选时间段和查询时间的车次情况
    '''

    def limit_time(self, dep_time, search_time):

        # 划分时间段
        part_1_s = datetime.datetime.strptime("00:00", "%H:%M").time()
        part_1_e = datetime.datetime.strptime("06:00", "%H:%M").time()
        part_2_s = datetime.datetime.strptime("06:00", "%H:%M").time()
        part_2_e = datetime.datetime.strptime("12:00", "%H:%M").time()
        part_3_s = datetime.datetime.strptime("12:00", "%H:%M").time()
        part_3_e = datetime.datetime.strptime("18:00", "%H:%M").time()
        part_4_s = datetime.datetime.strptime("18:00", "%H:%M").time()
        part_4_e = datetime.datetime.strptime("23:59", "%H:%M").time()

        d_t = ['0-6', '6-12', '12-18', '18-24']
        s_t = [114, 115, 117, 118]
        # 判断数据是否符合标准
        if dep_time not in d_t:
            print("Please select the right departure time ('0-6', '6-12', '12-18', '18-24')")
            return

        if search_time not in s_t:
            print("Please select the right search time (114, 115, 117, 118)")
            return

        # 下面这一段或许可优化，可以试试换成枚举
        if dep_time == '0-6':
            time_range = self.st_df[
                (self.st_df['出发时间'] >= part_1_s) & (self.st_df['出发时间'] < part_1_e) & (
                            self.st_df['查询时间'] == search_time)]

        elif dep_time == '6-12':
            time_range = self.st_df[
                (self.st_df['出发时间'] >= part_2_s) & (self.st_df['出发时间'] < part_2_e) & (
                        self.st_df['查询时间'] == search_time)]

        elif dep_time == '12-18':
            time_range = self.st_df[
                (self.st_df['出发时间'] >= part_3_s) & (self.st_df['出发时间'] < part_3_e) & (
                        self.st_df['查询时间'] == search_time)]

        elif dep_time == '18-24':
            time_range = self.st_df[
                (self.st_df['出发时间'] >= part_4_s) & (self.st_df['出发时间'] < part_4_e) & (
                        self.st_df['查询时间'] == search_time)]

        # rail_count = time_range['车次'].value_counts()

        # 统计车次情况
        rail_group = time_range[['车次', 'dep_to_dest']]['车次'].value_counts().sum().item()
        rail_ = time_range['车次'].value_counts()
        # 列车编号
        # ls_index = list(rail_group.index)
        #
        # '''
        #     rails的形式为： {'G2211': {'北京南站': 'destination': ['xx站', 'xx站', 'xx站']},
        #                     'G2222': {'北京站': 'destination': ['xx站', 'xx站', 'xx站']}}
        # '''
        # rails = {}
        # for i in ls_index:
        #     rails[i] = {}
        #     rail = time_range[(time_range['车次'] == i)]
        #     rail.sort_values(by=['出发时间'], inplace=True)
        #
        #     # 无重复的出发站
        #     dep_rail = rail['出发站'].unique()
        #
        #     for j in dep_rail:
        #         # 无重复的到达站
        #         tmp = rail[(rail['出发站'] == j)]['到达站'].unique()
        #         rails[i][j] = {'destination': list(tmp)}

        return rail_group, rail_

    """
    统计出发站和到达站分别的数量
    """
    def train_count(self):
        # 任务7
        rail_times_count_dep = self.st_df['出发站'].value_counts()
        rail_times_count_des = self.st_df['到达站'].value_counts()

        return rail_times_count_dep, rail_times_count_des

    # 任务7
    def convert_data(self, r):
        # 取索引
        r_t_c_i = list(r.index)
        # 转化为unicode
        r_t_c_i = [eval("u'%s'" % x) for x in r_t_c_i]
        # 取最大最小值
        max_num = r.iloc[0].item()
        min_num = r.iloc[-1].item()

        values = []
        for i in range(len(r_t_c_i)):
            # 取指定站点数据
            find = self.all_df[(self.all_df['站名'] == r_t_c_i[i])]
            # 取第一个数据的经度
            lng_m = find.loc[:, 'lng火星'].iloc[0].item()
            # 取第一个数据的纬度
            lat_m = find.loc[:, 'lat火星'].iloc[0].item()
            # 取统计的值
            v = r.iloc[i].item()
            # 装入一个list
            values.append([r_t_c_i[i], lng_m, lat_m, v])

        # 数据格式
        result = {
            'values': values,
            'max': max_num,
            'min': min_num
        }

        return result

    def _d_t_d(self, c1, c2):

        # 统计该字段中每一个元素出现的次数
        count_d = self.st_df['dep_to_dest'].value_counts()

        # 去重
        c2 = set(c2)
        c1 = set(c1)

        # 新建Dataframe表
        dep_dest_pd = pd.DataFrame(columns=c2, index=c1)
        # 获取索引，形式如 "上海-长春"
        ls_index = list(count_d.index)

        # 在新建表中添加数据
        for i in ls_index:
            a, b = i.split("-")
            dep_dest_pd.loc[b, a] = count_d.loc[i]

        dep_dest_pd = dep_dest_pd.replace(np.nan, 0)
        return dep_dest_pd

    """
    @:param city 指定城市
    """
    def train_track(self, city):
        # 调用函数_d_t_d
        d = self._d_t_d(self.st_df['des_city'].tolist(), self.st_df['dep_city'].tolist())

        d_l = d[city]
        # 取不为0的值
        d_l = d_l[d_l != 0]

        # 取索引，索引形式为：常州、泰州等
        d_l_i = list(d_l.index)
        d_list = []
        # 打包数据
        for i in d_l_i:
            d_list.append((city, i))

        # coord = pd.read_csv('./city_coordination.csv')
        geo_cities_coord = []
        # 准备散点图数据，形式为('城市': 值(int))
        scatter = []

        # 最大最小值，画图用
        max_num = max(d_l)
        min_num = min(d_l)

        for i in d_list:
            d_tmp = int(d_l[i[1]])
            scatter.append([i[1], d_tmp])

        convert_data = [d_list, scatter, max_num, min_num]
        return convert_data

    # 统计每个车次候补和无票的情况
    def _check(self, x):
        stock_count = 0
        x_list = x.tolist()
        for i in x_list:
            if i == '候补' or i == '--' or i == '*':
                stock_count += 1

        # 如果长度不相等则证明该车次还有余票所以应该返回1
        if stock_count != len(x_list):
            return 1

        # 无余票返回0 方便统计
        else:
            return 0

    # 声明一个函数，传入城市名 返回无余票车次占总车次的百分比如：0.6790883560164183
    def back_count(self, c):
        city3 = self.st_df[(self.st_df['dep_city'] == c)]
        tmp = city3[['商务座特等座', '软卧一等卧', '硬卧二等卧', '硬座']].apply(self._check, axis=1)
        # 这是一个Series
        counts = tmp.value_counts()

        # iloc即index_loc意思就是根据索引取数据
        return counts.iloc[0] / len(city3)

    def stock_analysis(self):
        # 拿到所有城市名并去重
        cities = self.st_df['dep_city'].unique()
        # 输出形式如：{'杭州', 0.6790883560164183}
        city_result = {}
        # 调用函数
        for c in cities:
            city_result[c] = self.back_count(c).item() * 100

        # 排序，key取字典的values
        sort_c = sorted(city_result.items(), key=lambda x: x[1], reverse=True)
        return sort_c

