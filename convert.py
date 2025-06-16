import numpy as np
import polars as pls
from schema import lg_schema, ys_schema

from project import gcj02towgs84

def ys2lg(ysdf):

  ysdf=ysdf.with_columns([
    pls.lit(0.0).alias("verticalAccuracy"),
    pls.lit(0).alias("isSplit"),
    pls.lit(0).alias("isMerge"),
    pls.lit(0).alias("isAdd"),
    pls.lit(0).alias("network"),
    pls.lit("").alias("networkName")
  ])

  ysdf = ysdf.with_columns([
    (pls.col("dataTime") * 1000).alias("geoTime"),
    (((pls.col("dataTime")+28800)//86400)*86400-28800).alias("dayTime"),
    (1-pls.col("locType")).alias("locationType"),
  ])

  ysdf=ysdf.rename({
    "dataTime": "groupTime",
    "heading": "course",
    "accuracy": "horizontalAccuracy"
  })

  ysdf = ysdf.select([
    "geoTime",
    "latitude",
    "longitude",
    "altitude",
    "course",
    "horizontalAccuracy",
    "verticalAccuracy",
    "speed",
    "dayTime",
    "groupTime",
    "isSplit",
    "isMerge",
    "isAdd",
    "network",
    "networkName",
    "locationType"
  ])

  return ysdf

def lg2ys(lgdf):

  lgdf=lgdf.rename({
    "groupTime": "dataTime",
    "course": "heading",
    "horizontalAccuracy": "accuracy"
  })

  lgdf=lgdf.with_columns([
    pls.lit(1).alias("isBackForeground"),
    pls.lit(0.0).alias("distance"),
    pls.lit(0).alias("stepType"),
    (pls.col("locationType")).alias("locType"),
  ])

  # Apply function and expand the result into two new columns
  lgdf = lgdf.with_columns(
      pls.struct(["longitude", "latitude"]).map_elements(
        lambda combined: gcj02towgs84(
          combined["longitude"], combined["latitude"]
        )
      ).alias("result")
  ).drop("longitude").drop("latitude")

  # "result" is now a list/tuple — extract into two separate columns
  lgdf = lgdf.with_columns([
      pls.col("result").list.get(0).alias("longitude"),
      pls.col("result").list.get(1).alias("latitude")
  ]).drop("result")

  lgdf = lgdf.select([
    "dataTime",
    "locType",
    "longitude",
    "latitude",
    "heading",
    "accuracy",
    "speed",
    "distance",
    "isBackForeground",
    "stepType",
    "altitude"
  ])



  return lgdf

def air2lg(airdf):
  airdf=airdf.with_columns([
    pls.lit(0.0).alias("verticalAccuracy"),
    pls.lit(1.0).alias("horizontalAccuracy"),
    pls.lit(0).alias("isSplit"),
    pls.lit(0).alias("isMerge"),
    pls.lit(0).alias("isAdd"),
    pls.lit(0).alias("network"),
    pls.lit("").alias("networkName"),
    pls.lit(0).alias("locationType")
  ])

  airdf = airdf.with_columns([
    (pls.col("Time") * 1000).alias("geoTime"),
    (((pls.col("Time")+28800)//86400)*86400-28800).alias("dayTime")
  ])

  airdf = airdf.rename({
    "Time": "groupTime",
    "Height": "altitude",
    "Angle": "course",
    "Speed": "speed",
    "Longitude": "longitude",
    "Latitude": "latitude",
  })

  airdf = airdf.select([
    "geoTime",
    "latitude",
    "longitude",
    "altitude",
    "course",
    "horizontalAccuracy",
    "verticalAccuracy",
    "speed",
    "dayTime",
    "groupTime",
    "isSplit",
    "isMerge",
    "isAdd",
    "network",
    "networkName",
    "locationType"
  ])

  return airdf

def air2ys(airdf):
  airdf=airdf.with_columns([
    pls.lit(1.0).alias("accuracy"),
    pls.lit(0.0).alias("distance"),
    pls.lit(0).alias("stepType"),
    pls.lit(1).alias("isBackForeground"),
    pls.lit(1).alias("locType")
  ])

  airdf=airdf.rename({
    "Time": "dataTime",
    "Height": "altitude",
    "Angle": "heading",
    "Speed": "speed",
    "Longitude": "longitude",
    "Latitude": "latitude",
  })

  airdf = airdf.select([
    "dataTime",
    "locType",
    "longitude",
    "latitude",
    "heading",
    "accuracy",
    "speed",
    "distance",
    "isBackForeground",
    "stepType",
    "altitude"
  ])

  return airdf