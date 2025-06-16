  
from pathlib import Path
import polars as pls
from schema import air_schema
from convert import air2ys
def merge_air_route(merged_df):

  merged_selected = merged_df

  air_paths = Path("./flights")
  for file_path in air_paths.rglob("*.csv"):
      air_df = pls.read_csv(file_path, schema=air_schema)

      air_df = air2ys(air_df)

      min_time = air_df.select(pls.col("dataTime").min())[0,0]
      max_time = air_df.select(pls.col("dataTime").max())[0,0]

      print("{}:{}".format((max_time-min_time) // 3600, ((max_time-min_time)//60) % 60))

      merged_selected = merged_selected.filter(pls.col("dataTime").is_between(min_time, max_time).not_())

      merged_selected = pls.concat([merged_selected, air_df], how="vertical")

  return merged_selected

if __name__ == "__main__":
   
  merge_air_route(None)