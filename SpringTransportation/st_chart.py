from pyecharts.charts import Geo, Bar
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.globals import GeoType


class stChart:
    def port_dis(self, x):
        p = Geo(init_opts=opts.InitOpts(width='2000px', height='1300px'))

        p.add_schema(maptype='china')

        data_pair_1 = []
        data_pair_2 = []
        for i in x[0]['values']:
            p.add_coordinate(i[0], i[1], i[2])
            data_pair_1.append((i[0], i[3]))

        for i in x[1]['values']:
            p.add_coordinate(i[0], i[1], i[2])
            data_pair_2.append((i[0], i[3]))

        # print(data_pair)

        p.add(
            '到达站',
            type_=GeoType.SCATTER,
            data_pair=data_pair_2,
            symbol_size=6,
            color='#5A78D4',
            # encode={'value': 2},
            label_opts=opts.LabelOpts(position='right', is_show=False, formatter=JsCode(
                """
                function(params){
                if ('value' in params.data){
                        return params.data.value[2]
                    }
                }
                """
            )
                                      )
        )
        p.add(
            '出发站',
            type_=GeoType.SCATTER,
            data_pair=data_pair_1,
            symbol_size=6,
            # color='#FF6347',
            # encode={'value': 2},
            label_opts=opts.LabelOpts(position='right', is_show=False, formatter=JsCode(
                """
                function(params){
                if ('value' in params.data){
                        return params.data.value[2]
                    }
                }
                """
            )
                                      )
        )
        p.set_global_opts(
            legend_opts=opts.LegendOpts(is_show=True, type_='plain'),
            visualmap_opts=opts.VisualMapOpts(
                # pos_top='10',
                # pos_left='10',
                type_='size',
                range_size=[5, 65],
                max_=x[0]['max'] + 100,
                is_piecewise=False,
                # pieces=[
                #     {"max": x[2], "min": 0, "label": ""}
                # ]
            )
        )
        return p

    def train_track(self, x, name):
        t = (
            Geo(init_opts=opts.InitOpts(width='2000px', height='1300px', bg_color='#696969'))
            .add_schema(maptype='china')
            # .add(
            #     '',
            #     type_='lines',
            #     is_polyline=True,
            #     data_pair=x,
            #     linestyle_opts=opts.LineStyleOpts(opacity=0.2, width=1, color='#5A94DF'),
            #     progressive_threshold=500,
            #     progressive=200,
            # )
            .add(
                name,
                type_='scatter',
                data_pair=x[1],
                symbol_size=6,
                encode={'value': 2},
                label_opts=opts.LabelOpts(color='#5A78D4', position='right', is_show=False, formatter=JsCode(
                    """
                    function(params){
                    if ('value' in params.data){
                            return params.data.value[2]
                        }
                    }
                    """
                )),

            )
            .add(
                name,
                type_='lines',
                is_polyline=True,
                data_pair=x[0],
                linestyle_opts=opts.LineStyleOpts(width=0),
                effect_opts=opts.EffectOpts(color='#F08080', is_show=True, trail_length=0.5, symbol_size=2),
            )
            .set_global_opts(
                legend_opts=opts.LegendOpts(is_show=True, type_='plain'),
                visualmap_opts=opts.VisualMapOpts(
                    # pos_top='10',
                    # pos_left='10',
                    type_='size',
                    range_size=[5, 60],
                    max_=x[2] + 100,
                    is_piecewise=False,
                    # pieces=[
                    #     {"max": x[2], "min": 0, "label": ""}
                    # ]
                )
            )
        )
        return t

    def bar_chart(self, x):
        cate = ['1月14日', '1月15日', '1月17日', '1月18日']
        b = (
            Bar(init_opts=opts.InitOpts(width='2000px', height='1300px'))
            .add_xaxis(cate)
            .add_yaxis('0时-6时', x[0])
            .add_yaxis('6时-12时', x[1])
            .add_yaxis('12时-18时', x[2])
            .add_yaxis('18时-24时', x[3])
        )

        return b

    def bar_chart_stock(self, name, value):
        cate = name
        b = Bar(init_opts=opts.InitOpts(width='2000px', height='1300px'))
        b.add_xaxis(cate)
        b.add_yaxis('百分比', value, color='#BA55D3')
        b.set_global_opts(title_opts=opts.TitleOpts(title='出发城市无票率'))

        return b

