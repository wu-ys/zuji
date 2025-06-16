import polars as pls

lg_schema = {
  "geoTime":pls.Int64,
  "latitude": pls.Float64,
  "longitude": pls.Float64,
  "altitude": pls.Float64,
  "course": pls.Float64,
  "horizontalAccuracy": pls.Float64,
  "verticalAccuracy": pls.Float64,
  "speed": pls.Float64,
  "dayTime": pls.Int64,
  "groupTime": pls.Int64,
  "isSplit": pls.Int32,
  "isMerge": pls.Int32,
  "isAdd": pls.Int32,
  "network": pls.Int32,
  "networkName": pls.Utf8,
  "locationType": pls.Int32
}

ys_schema = {
  "dataTime":pls.Int64,
  "locType": pls.Int32,
  "longitude": pls.Float64,
  "latitude": pls.Float64,
  "heading": pls.Float64,
  "accuracy": pls.Float64,
  "speed": pls.Float64,
  "distance": pls.Float64,
  "isBackForeground": pls.Int32,
  "stepType": pls.Int32,
  "altitude": pls.Float64
}

air_schema = {
  "Time": pls.Int64,
  "UTC TIME": pls.Utf8,
  "Anum": pls.Utf8,
  "Fnum": pls.Utf8,
  "Height": pls.Float64,
  "Speed": pls.Float64,
  "Angle": pls.Float64,
  "Longitude":pls.Float64,
  "Latitude":pls.Float64
}
