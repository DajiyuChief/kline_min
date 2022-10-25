import efinance as ef
import tushare as ts
from pyecharts import options as opts
from pyecharts.charts import Kline, Bar, Grid, Line
from pyecharts.commons.utils import JsCode
from getstockname import get_name

pro = ts.set_token('f558cbc6b24ed78c2104e209a8a8986b33ec66b7c55bcfa2f46bc108')

# 股票代码
stock_code = '000001'
# 5 分钟
frequency = 5
df = ef.stock.get_quote_history(stock_code, klt=frequency)
# df2 = ts.get_hist_data('000001')
df4 = ts.pro_bar(ts_code='600000.SH', freq='5min', start_date='2022-10-24 09:00:00', end_date='2022-10-25 15:00:00')


# df3 = ts.pro_bar(ts_code='000001.SZ', freq='5min')


def plot_kline_volume(data, name, freq):
    kline = (
        Kline(init_opts=opts.InitOpts(width="1800px", height="1000px"))
        .add_xaxis(xaxis_data=list(data.index))
        .add_yaxis(
            series_name="klines",
            y_axis=data[["开盘", "收盘", "最低", "最高"]].values.tolist(),
            itemstyle_opts=opts.ItemStyleOpts(color="#ec0000", color0="#00da3c"),
        )
        .set_global_opts(legend_opts=opts.LegendOpts(is_show=True, pos_bottom=10, pos_left="center"),
                         datazoom_opts=[
                             opts.DataZoomOpts(
                                 is_show=False,
                                 type_="inside",
                                 xaxis_index=[0, 1],  # 这里需要修改可缩放的x轴坐标编号
                                 range_start=98,
                                 range_end=100,
                             ),
                             opts.DataZoomOpts(
                                 is_show=True,
                                 xaxis_index=[0, 1],  # 这里需要修改可缩放的x轴坐标编号
                                 type_="slider",
                                 pos_top="85%",
                                 range_start=98,
                                 range_end=100,
                             ),
                         ],
                         yaxis_opts=opts.AxisOpts(
                             is_scale=True,
                             splitarea_opts=opts.SplitAreaOpts(
                                 is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                             ),
                         ),
                         tooltip_opts=opts.TooltipOpts(
                             trigger="axis",
                             axis_pointer_type="cross",
                             background_color="rgba(245, 245, 245, 0.8)",
                             border_width=1,
                             border_color="#ccc",
                             textstyle_opts=opts.TextStyleOpts(color="#000"),
                         ),
                         visualmap_opts=opts.VisualMapOpts(
                             is_show=False,
                             dimension=2,
                             series_index=5,
                             is_piecewise=True,
                             pieces=[
                                 {"value": 1, "color": "#00da3c"},
                                 {"value": -1, "color": "#ec0000"},
                             ],
                         ),
                         axispointer_opts=opts.AxisPointerOpts(
                             is_show=True,
                             link=[{"xAxisIndex": "all"}],
                             label=opts.LabelOpts(background_color="#777"),
                         ),
                         brush_opts=opts.BrushOpts(
                             x_axis_index="all",
                             brush_link="all",
                             out_of_brush={"colorAlpha": 0.1},
                             brush_type="lineX",
                         ),
                         title_opts=opts.TitleOpts(
                             title=name,
                             pos_left='center',
                             title_textstyle_opts=opts.TextStyleOpts(
                                 font_size=30
                             )),
                         )
    )

    bar = (
        Bar()
        .add_xaxis(xaxis_data=list(data.index))
        .add_yaxis(
            series_name="volume",
            y_axis=data["成交量"].tolist(),
            xaxis_index=1,
            yaxis_index=1,
            label_opts=opts.LabelOpts(is_show=False),
            itemstyle_opts=opts.ItemStyleOpts(
                color=JsCode(
                    """
                function(params) {
                    var colorList;
                    if (barData[params.dataIndex][1] > barData[params.dataIndex][0]) {
                        colorList = '#ef232a';
                    } else {
                        colorList = '#14b143';
                    }
                    return colorList;
                }
                """
                )
            ),
        )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                type_="category",
                grid_index=1,
                axislabel_opts=opts.LabelOpts(is_show=False),
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )

    # kline.render("kline.html")   #test

    grid_chart = Grid(
        init_opts=opts.InitOpts(
            width="1800px",
            height="1000px",
            animation_opts=opts.AnimationOpts(animation=False),
        )
    )

    grid_chart.add_js_funcs(
        "var barData={}".format(data[["开盘", "收盘"]].values.tolist()))  # 导入open、close数据到barData改变交易量每个bar的颜色
    grid_chart.add(
        # overlap_kline_line,
        kline,
        grid_opts=opts.GridOpts(pos_left="10%", pos_right="8%", height="40%"),
    )
    grid_chart.add(
        bar,
        grid_opts=opts.GridOpts(
            pos_left="10%", pos_right="8%", pos_top="60%", height="20%"
        ),
    )
    grid_chart.render("kline_volume"+str(freq)+"min"+".html")


def generate_html():
    stockcode = input()
    freq = int(input())
    data = ef.stock.get_quote_history(stockcode, klt=freq)  # 将数据按照时间排序
    data.set_index(["日期"], inplace=True)  # 设置日期为索引
    name = get_name(stockcode)
    plot_kline_volume(data, name, freq)


generate_html()
