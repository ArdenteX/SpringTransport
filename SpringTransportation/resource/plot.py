from pyecharts.charts import BMap
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from bs4 import BeautifulSoup


def train_track(x):
    t = (
        BMap(init_opts=opts.InitOpts(width='100%', height='1500px'))
        .add_schema(
            baidu_ak='uZOwI593w9RiXMURr36tLnrYCYLbm8EN',
            center=[104.114129, 37.550339],
            zoom=5,
            is_roam=True,
            map_style={
                'styleJson': [
                {
                  'featureType': 'water',
                  'elementType': 'all',
                  'stylers': {
                    'color': '#031628'
                  }
                },
                {
                  'featureType': 'land',
                  'elementType': 'geometry',
                  'stylers': {
                    'color': '#000102'
                  }
                },
                {
                  'featureType': 'highway',
                  'elementType': 'all',
                  'stylers': {
                    'visibility': 'off'
                  }
                },
                {
                  'featureType': 'arterial',
                  'elementType': 'geometry.fill',
                  'stylers': {
                    'color': '#000000'
                  }
                },
                {
                  'featureType': 'arterial',
                  'elementType': 'geometry.stroke',
                  'stylers': {
                    'color': '#0b3d51'
                  }
                },
                {
                  'featureType': 'local',
                  'elementType': 'geometry',
                  'stylers': {
                    'color': '#000000'
                  }
                },
                {
                  'featureType': 'railway',
                  'elementType': 'geometry.fill',
                  'stylers': {
                    'color': '#000000'
                  }
                },
                {
                  'featureType': 'railway',
                  'elementType': 'geometry.stroke',
                  'stylers': {
                    'color': '#08304b'
                  }
                },
                {
                  'featureType': 'subway',
                  'elementType': 'geometry',
                  'stylers': {
                    'lightness': -70
                  }
                },
                {
                    'featureType': 'building',
                    'elementType': 'geometry.fill',
                    'stylers': {
                    'color': '#000000'
                  }
                },
                {
                  'featureType': 'all',
                  'elementType': 'labels.text.fill',
                  'stylers': {
                    'color': '#857f7f'
                  }
                },
                {
                  'featureType': 'all',
                  'elementType': 'labels.text.stroke',
                  'stylers': {
                    'color': '#000000'
                  }
                },
                {
                  'featureType': 'building',
                  'elementType': 'geometry',
                  'stylers': {
                    'color': '#022338'
                  }
                },
                {
                  'featureType': 'green',
                  'elementType': 'geometry',
                  'stylers': {
                    'color': '#062032'
                  }
                },
                {
                  'featureType': 'boundary',
                  'elementType': 'all',
                  'stylers': {
                    'color': '#465b6c'
                  }
                },
                {
                  'featureType': 'manmade',
                  'elementType': 'all',
                  'stylers': {
                    'color': '#022338'
                  }
                },
                {
                  'featureType': 'label',
                  'elementType': 'all',
                  'stylers': {
                    'visibility': 'off'
                  }
                }
                ]
            }
        )
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
            '车次',
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
            '',
            type_='lines',
            is_polyline=True,
            data_pair=x[0],
            linestyle_opts=opts.LineStyleOpts(width=0, color='red'),
            effect_opts=opts.EffectOpts(color='#F08080', is_show=True, trail_length=0.5, symbol_size=2),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False, type_='plain'),
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

        .render('test1.html')
    )

