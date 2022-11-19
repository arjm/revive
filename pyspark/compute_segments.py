#!/usr/bin/env python

"""compute_segments.py: This class is responsible to create customer segments based on the input data"""

__author__      = "Arjit Malviya"

import mysql.connector

from pyspark.sql import Window
from pyspark.sql.functions import *
from pyspark.sql.functions import row_number

from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession

def create_frequent_segment(df_voucher_logs):
      """Created frequency based segement based on number of orders for customer"""
      df_voucher_logs_peru = df_voucher_logs.filter(
            "country_code == 'Peru' AND voucher_amount is not null AND total_orders > 0")

      df_voucher_logs_peru.orderBy("voucher_amount", ascending=False).filter(col("total_orders").cast("int").isNotNull()).show()
      df_voucher_logs_peru_grouped = df_voucher_logs_peru.groupBy("total_orders", "voucher_amount").count()


      w = Window.partitionBy("total_orders").orderBy(col("count").desc())

      df_voucher_peru_final = df_voucher_logs_peru_grouped.withColumn("row",row_number().over(w)).filter(col("row") == 1).drop("row")

      save_to_mysql(df_voucher_peru_final)


def create_recency_segement(df_voucher_logs):
      """Created frequency based segement based on days since last customer order by a customer"""
      return

def save_to_mysql(data_frame_to_save):
      """Export data into MySQL db. Database must be created before performing this operation"""
      data_frame_to_save.write.format('jdbc').options(\
            url='jdbc:mysql://mysql/campaign',\
            driver='com.mysql.jdbc.Driver',
            dbtable='voucher_log',\
            user='root',\
            password='root').mode('overwrite').save()


sc = SparkContext.getOrCreate();
spark = SparkSession(sc)

df_voucher_logs = spark.read.parquet("data.parquet.gzip")
create_frequent_segment(df_voucher_logs)
create_recency_segement(df_voucher_logs)