"""One visual vocabulary, exactly eight primary plot families."""
import plotly.express as px
import plotly.graph_objects as go

COLORS = ["#4E89A8", "#6A9F94", "#8795BE", "#BD89AB", "#D3A16D", "#6C9CB8", "#A59B83", "#92A3B2"]
BASE = dict(template="plotly_white", colorway=COLORS, font=dict(family="Arial", size=13),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")


def polish(fig, title, height=420):
    fig.update_layout(**BASE, title=dict(text=title, font=dict(size=19)), height=height,
                      margin=dict(l=20, r=20, t=68, b=25), legend_title_text="")
    return fig


def line(df, x, y, color=None, title="Historical demand"):
    return polish(px.line(df, x=x, y=y, color=color, color_discrete_sequence=COLORS, markers=False), title)


def bar(df, x, y, title="Regional comparison"):
    return polish(px.bar(df, x=x, y=y, orientation="h", color=x,
                         color_continuous_scale="Tealgrn"), title)


def area(df, x, y, color, title="Generation mix"):
    return polish(px.area(df, x=x, y=y, color=color, color_discrete_sequence=COLORS), title)


def heatmap(table, title="Hourly demand"):
    return polish(px.imshow(table, aspect="auto", color_continuous_scale="YlOrRd",
                            labels={"x": "Hour of day", "y": "Day of week", "color": "MW"}), title)


def box(df, x, y, title="Seasonality and variability"):
    return polish(px.box(df, x=x, y=y, points=False, color=x,
                        color_discrete_sequence=COLORS), title)


def scatter(df, x, y, color, title="Relationships"):
    return polish(px.scatter(df, x=x, y=y, color=color, opacity=.48, render_mode="webgl",
                             color_discrete_sequence=COLORS,
                             hover_data=[c for c in ("date",) if c in df]), title)


def histogram(df, x, title="Demand distribution"):
    return polish(px.histogram(df, x=x, nbins=55, color_discrete_sequence=[COLORS[3]],
                               marginal="rug" if len(df) < 1200 else None), title)


def map_markers(df, title="Regional demand map"):
    fig = px.scatter_geo(df, lat="lat", lon="lon", size="size",
                         color="value", hover_name="region",
                         color_continuous_scale="Turbo", size_max=33,
                         hover_data={"size": False, "value": ":,.0f"})
    fig.update_geos(lataxis_range=[41, 52], lonaxis_range=[-6, 10],
                    showcountries=True, showland=True,
                    landcolor="#E6EFF4", countrycolor="#B2C4D0")
    return polish(fig, title, 500)
