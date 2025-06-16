# zuji

用于合并灵感足迹、一生足迹与航班飞行路径

## Requirements

- polars (pola.rs)

## 如何使用

1. 将灵感足迹与一生足迹导出的csv文件放在本目录下，分别命名为lgzj.csv与yszj.csv
2. 目前支持将灵感足迹格式数据转换为一生足迹格式数据，并补充一生足迹中缺失日期的数据
3. 运行merge.py，输出为两份文件合并后，一生足迹格式的数据，可直接导入一生足迹

## 飞行路径

从variflight ADSB (alightadsb.variflight.com) 中查询对应日期航班，下载csv文件数据至./flights文件夹，之后运行merge.py即可将飞行路径加入合并后的文件中。
