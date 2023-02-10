# drawBotGrid

**drawBotGrid** is a small library that make grid based layout easy in the always amazing [DrawBot](https://www.drawbot.com).

![](/drawBotGrid/docs/columns_0.png)


## ColumnGrid

A `ColumnGrid` dived the page in columns, separated by a gutter, making it easy to retrieve absolute x coordinates

```python
newPage("A4Landscape")
columns = ColumnGrid((50, 50, 742, 495), subdivisions=8, gutter=10)

fill(0, 1, 0, .5)
rect(columns[1], 100, columns * 3, 300)

columns.draw(show_index=True)
```

![](/drawBotGrid/docs/columns_1.png)
