import logging
import os
import boto3
import calendar
import csv
from botocore.exceptions import ClientError
from datetime import datetime

logger = logging.getLogger(__name__)

BUCKET = "noaa-jpss"
PREFIX = "JPSS_Blended_Products/VFM_5day_GLB/ShapeZIP/"
PATTERN = ["GLB085", "GLB086"]
HEADERS = ["Filenames", "Year"]


class ObjectWrapper:
    def __init__(self, s3_object) -> None:
        self.object = s3_object
        self.key = self.object.key

    @staticmethod
    def list(bucket, prefix=None):
        try:
            if not prefix:
                objects = list(bucket.objects.all())
            else:
                objects = list(bucket.objects.filter(Prefix=prefix))
            logger.info(
                "Got objects %s from bucket '%s'", [o.key for o in objects], bucket.name
            )
        except ClientError:
            logger.exception("Could not get objects for bucket '%s'", bucket.name)
            raise
        else:
            return objects


yearly_prefixes = [
    "JPSS_Blended_Products/VFM_5day_GLB/ShapeZIP/2012/",
    "JPSS_Blended_Products/VFM_5day_GLB/ShapeZIP/2013/",
    "JPSS_Blended_Products/VFM_5day_GLB/ShapeZIP/2014/",
    "JPSS_Blended_Products/VFM_5day_GLB/ShapeZIP/2015/",
    "JPSS_Blended_Products/VFM_5day_GLB/ShapeZIP/2016/",
    "JPSS_Blended_Products/VFM_5day_GLB/ShapeZIP/2017/",
    "JPSS_Blended_Products/VFM_5day_GLB/ShapeZIP/2018/",
    "JPSS_Blended_Products/VFM_5day_GLB/ShapeZIP/2019/",
    "JPSS_Blended_Products/VFM_5day_GLB/ShapeZIP/2020/",
    "JPSS_Blended_Products/VFM_5day_GLB/ShapeZIP/2023/",
]

month_list = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

days = [5, 10, 15, 20, 25, 30]

client = boto3.client("s3")


def prefix_list(prefix):
    response = client.list_objects_v2(
        Bucket=BUCKET,
        Prefix=prefix,
        Delimiter="/",
    )
    prefixes = []
    if "CommonPrefixes" in response:
        prefixes = [prefix["Prefix"] for prefix in response["CommonPrefixes"]]
    return prefixes


def folder_path(prefix):
    (abs_path, file_name) = os.path.split(prefix)
    dir = os.path.basename(abs_path)
    return dir


def list_objects(prefix):
    response = client.list_objects_v2(
        Bucket=BUCKET,
        Prefix=prefix,
        Delimiter="/",
    )
    objects = []
    if "Contents" in response:
        objects = [obj["Key"] for obj in response["Contents"]]
    return objects


def extract_filenames_with_pattern(date: datetime):
    print("Extracting file patterns ", PATTERN, " for given date: ", date.date())
    prefix = (
        PREFIX
        + str(date.year)
        + "/"
        + str(date.month).zfill(2)
        + "/"
        + str(date.day).zfill(2)
        + "/"
    )
    objects = list_objects(prefix)
    filtered_list = []
    for pat in PATTERN:
        matched = [os.path.basename(obj).split(".")[0] for obj in objects if pat in obj]
        filtered_list.extend(matched)
    print(
        "Found files ",
        filtered_list,
        " with pattern ",
        PATTERN,
        " for given date: ",
        date.date(),
    )
    return filtered_list


def export_to_csv(data: list, year: int = None):
    mode = "w" if not year else "a"
    with open("filenames.csv", mode, newline="") as file:
        writer = csv.writer(file)
        if year:
            for filename in data:
                writer.writerow([filename, year])
        else:
            writer.writerow(data)


def every_fifth_day_of_every_month_in_a_year(year: int):
    filenames = []

    # Retrieves monthly prefixes from S3 bucket for a given year
    monthly_prefixes = prefix_list(PREFIX + str(year) + "/")

    # Retrieves list of months from the prefixes
    months = [int(folder_path(prefix)) for prefix in monthly_prefixes]

    for month in months:
        for day in days:
            try:
                # Calculate every fifthe day of the month
                current_date = datetime(year, month, day)
            except ValueError:
                # Handles fifth day for the month of February
                last_day = calendar.monthrange(year, month)
                current_date = datetime(year, month, last_day[1])
            # five_day_list.append(current_date)
            extracted = extract_filenames_with_pattern(current_date)
            filenames.extend(extracted)
    export_to_csv(filenames, year)


def usage():
    export_to_csv(HEADERS)
    # client = boto3.client("s3")
    # response = client.list_objects_v2(
    #     Bucket="noaa-jpss",
    #     Prefix="JPSS_Blended_Products/VFM_5day_GLB/ShapeZIP/",
    #     Delimiter="/",
    # )
    years = []
    # if "CommonPrefixes" in response:
    #     yearly_prefixes = [prefix["Prefix"] for prefix in response["CommonPrefixes"]]
    #     for prefix in yearly_prefixes:
    #         year = folder_path(prefix)
    #         years.append(year)
    #         print(prefix)
    for prefix in yearly_prefixes:
        year = int(folder_path(prefix))
        years.append(year)
        every_fifth_day_of_every_month_in_a_year(year)


if __name__ == "__main__":
    usage()
