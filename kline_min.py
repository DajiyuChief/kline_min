import efinance as ef
import tushare as ts
from pyecharts import options as opts
from pyecharts.charts import Kline, Bar, Grid, Line, Tab, Timeline
from pyecharts.commons.utils import JsCode
from only_kline import plot_kline,grid

pro = ts.set_token('f558cbc6b24ed78c2104e209a8a8986b33ec66b7c55bcfa2f46bc108')


def generate_kline(data) -> Kline:
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
                         # title_opts=opts.TitleOpts(
                         #     title=name,
                         #     pos_left='center',
                         #     title_textstyle_opts=opts.TextStyleOpts(
                         #         font_size=30
                         #     )),
                         )
    )
    return kline


def generate_bar(data) -> Bar:
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
    return bar

    # kline.render("kline.html")   #test


def grid_mutil(data) -> Grid:
    kline = generate_kline(data)
    bar = generate_bar(data)
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
    ),
    grid_chart.add(
        bar,
        grid_opts=opts.GridOpts(
            pos_left="10%", pos_right="8%", pos_top="60%", height="20%"
        ),
    )
    # grid_chart.render("kline_volume" + str(freq) + "min" + ".html")
    return grid_chart


def multi_kline(data, name):
    tab = Tab()
    tab.add(grid_mutil(data), "5min_kline")
    tab.add(grid_mutil(data), "15min_kline")
    tab.add(grid_mutil(data), "30min_kline")
    tab.add(grid_mutil(data), "60min_kline")
    tab.render("tab_base.html")


def generate_html():
    tab = Tab()
    stockcode = input()
    # name = get_name(stockcode)
    data_5min = ef.stock.get_quote_history(stockcode, klt=5)
    data_5min.set_index(["日期"], inplace=True)
    data_15min = ef.stock.get_quote_history(stockcode, klt=15)
    data_15min.set_index(["日期"], inplace=True)
    data_30min = ef.stock.get_quote_history(stockcode, klt=30)
    data_30min.set_index(["日期"], inplace=True)
    data_60min = ef.stock.get_quote_history(stockcode, klt=60)
    data_60min.set_index(["日期"], inplace=True)
    tab.add(grid(data_5min), "5min")
    tab.add(grid(data_15min), "15min")
    tab.add(grid(data_30min), "30min")
    tab.add(grid(data_60min), "60min")
    #
    # for freq in [5, 15, 30, 60]:
    #     data = ef.stock.get_quote_history(stockcode, klt=freq)  # 将数据按照时间排序
    #     data.set_index(["日期"], inplace=True)  # 设置日期为索引
    #     tab.add(grid_mutil(data), str(freq) + "min_kline")
    # tab.render("min_kline.html")
    tab.render("min_kline.html")


generate_html()
