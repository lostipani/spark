import os
import logging
from typing import Dict, Any

from pyspark.sql import SparkSession
from pyspark.sql import types as T

logging.basicConfig(
    format="%(message)s",
    level=os.getenv("LOG_LEVEL", "INFO"),
)
logger = logging.getLogger()


class Loader(object):
    """
    Instantiate a Spark dataframe and fill it with data.

    Args
        master_URL (str): Spark master instance's URL
        sleep (float): sleep time
    """

    def __init__(self, master_URL: str, sleep: float):
        self.master = master_URL
        self.sleep = sleep

    def load(self, data: Dict[Any, Any]):
        """
        The loader stores data in the pyspark dataframe.
        
        Args
            data
        """
        newRow = self.spark.createDataFrame([data], schema=self._infer_schema())
        self.df = self.df.union(newRow)
        logger.debug(self.df.show())

    def setup_spark(self):
        """
        Close pending session, build a new session, create an empty dataframe.
        """
        SparkSession.builder.master(self.master).getOrCreate().stop()
        self.spark = SparkSession.builder.master(self.master).getOrCreate()
        self.df = self.spark.createDataFrame([], schema=self._infer_schema())

    def _infer_schema(self):
        return T.StructType(
            [
                T.StructField("A", T.StringType()),
                T.StructField("B", T.StringType()),
                T.StructField("C", T.StringType()),
            ]
        )


def main():
    loader = Loader(os.environ["SPARK_MASTER"], float(os.environ["SLEEP"]))
    loader.setup_spark()
    loader.load({0: "qsdqsd", 1: "ezaeza", 2: "hjlfoe"})


if __name__ == "__main__":
    main()
