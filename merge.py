import numpy as np

import polars as pls

from schema import lg_schema, ys_schema
from convert import *

from pathlib import Path

from air import merge_air_route

if __name__ == "__main__":

  lgdf = pls.read_csv("./lgzj.csv", n_rows=1000000,
  schema_overrides=lg_schema).filter(pls.col("locationType")==0)

  ysdf = pls.read_csv("./yszj.csv", n_rows=1000000, schema_overrides=ys_schema)

  ysdf_date = ysdf.select([
    (pls.col("dataTime")*1000 + 8*60*60).cast(pls.Datetime("ms")).dt.date().alias("date")
  ])

  lgdf_date = lgdf.select([
    (pls.col("geoTime") + 8*60*60).cast(pls.Datetime("ms")).dt.date().alias("date"),
  ])

  full_range = pls.select( pls.date_range(
    start= ysdf_date.select(pls.col("date").min())[0,0],
    end= ysdf_date.select(pls.col("date").max())[0,0],
    interval="1d"
  ).alias("date0"))

  missing_dates_lg = pls.select(
    full_range.filter(~pls.col("date0").is_in(lgdf_date["date"]))
  )
  print("Miss dates in Linggan Zuji:")
  print(missing_dates_lg)

  missing_dates_ys = pls.select(
    full_range.filter(~pls.col("date0").is_in(ysdf_date["date"]))
  )
  print("Miss dates in Yisheng Zuji:")
  print(missing_dates_ys)

  ys_lgdf = lg2ys(lgdf)
  ys_lgdf_date = ys_lgdf.with_columns([
    (pls.col("dataTime")*1000 + 8*60*60).cast(pls.Datetime("ms")).dt.date().alias("date")
  ])

  print(ys_lgdf_date)
  lgdf_selected = ys_lgdf_date.filter(pls.col("date").is_in(missing_dates_ys["date0"])).drop("date")

  ysdf_merged = pls.concat([ysdf, lgdf_selected], how="vertical")

  ysdf_merged = merge_air_route(ysdf_merged)

  ysdf_merged.write_csv("merged_air.csv")