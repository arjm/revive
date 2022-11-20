#!/usr/bin/env python

"""compute_segments.py: This class is responsible to create customer segments based on the input data"""

__author__      = "Arjit Malviya"

import mysql.connector

from pyspark.sql import Window
from pyspark.sql.functions import *
from pyspark.sql.functions import row_number

from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession

SQL_TABLE_FREQUENT_SEGEMENT = "voucher_frequent_segment"
SQL_TABLE_RECENCY_SEGEMENT = "voucher_recency_segment"

def create_frequent_segment(df_voucher_logs, countries):
      """Created frequency based segement based on number of orders for customer"""
      df_voucher_logs_filtered = df_voucher_logs.where(col("country_code").isin (countries))\
            .filter("voucher_amount is not null AND total_orders > 0")

      df_voucher_logs_filtered_ordered = df_voucher_logs_filtered.orderBy("voucher_amount", ascending=False)\
            .filter(col("total_orders").cast("int").isNotNull())
      df_voucher_logs_grouped = df_voucher_logs_filtered_ordered.groupBy("total_orders", "voucher_amount").count()

      w = Window.partitionBy("total_orders").orderBy(col("count").desc())

      df_voucher_final = df_voucher_logs_grouped\
            .withColumn("row",row_number().over(w)).filter(col("row") == 1).drop("row")

      save_to_mysql(df_voucher_final, SQL_TABLE_FREQUENT_SEGEMENT)


def create_recency_segement(df_voucher_logs, countries):
      """Created frequency based segement based on days since last customer order by a customer"""

      df_voucher_logs_peru = df_voucher_logs.where(col("country_code").isin (countries))\
            .filter("voucher_amount is not null AND total_orders > 0")

      import pyspark.sql.functions as F
      df_voucher_logs_days_filtered = df_voucher_logs_peru.withColumn('days_since', \
            F.datediff(df_voucher_logs.last_order_ts, df_voucher_logs.first_order_ts))

      df_voucher_logs_days_filtered_ordered = df_voucher_logs_days_filtered.orderBy("voucher_amount", ascending=False)\
            .filter(col("days_since").cast("int").isNotNull())
      df_voucher_logs_days_grouped = df_voucher_logs_days_filtered_ordered\
            .groupBy("days_since", "voucher_amount").count()

      w = Window.partitionBy("days_since").orderBy(col("count").desc())
      df_voucher_final = df_voucher_logs_days_grouped\
            .withColumn("row",row_number().over(w)).filter(col("row") == 1).drop("row")

      save_to_mysql(df_voucher_final, SQL_TABLE_RECENCY_SEGEMENT)

def save_to_mysql(data_frame_to_save, table_name):
      """Export data into MySQL db. Database must be created before performing this operation"""
      data_frame_to_save.write.format('jdbc').options(\
            url='jdbc:mysql://mysql/campaign',\
            driver='com.mysql.jdbc.Driver',
            dbtable=table_name,\
            user='root',\
            password='root').mode('overwrite').save()


sc = SparkContext.getOrCreate();
spark = SparkSession(sc)

df_voucher_logs = spark.read.parquet("data.parquet.gzip")

countries_filter = ['Peru']
create_frequent_segment(df_voucher_logs, countries_filter)
create_recency_segement(df_voucher_logs, countries_filter)
print("Batch pipeline completed successfully!")
