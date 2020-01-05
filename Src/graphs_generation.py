import plotly.graph_objects as go
Followers=['10000+', '5000-10000', '1000-5000','500-1000','200-500','100-200','50-100','0-50']
positive = [21, 41, 83, 121, 198, 245,521, 234]
negative = [5,6, 17, 63, 71,103,358,371]
fig = go.Figure(data=[
    go.Bar(name='positive', x=Followers, y=positive),
    go.Bar(name='negative', x=Followers, y=negative)
])
# Change the bar mode
fig.update_layout(barmode='group')
fig.show()