import os
import boto3
import calendar
import csv
from datetime import datetime, timedelta
from conf import config

# S3 client for API operations
client = boto3.client("s3")


def prefix_list(prefix: str):
    """Retrieves list of sub folders for a given folder in a s3 bucket

    Args:
        prefix (str): folder prefix in a s3 bucket

    Returns:
        list: list of sub folders
    """
    response = client.list_objects_v2(
        Bucket=config.BUCKET,
        Prefix=prefix,
        Delimiter="/",
    )
    prefixes = []
    if "CommonPrefixes" in response:
        prefixes = [prefix["Prefix"] for prefix in response["CommonPrefixes"]]
    return prefixes


def folder_path(prefix: str):
    """Retrieves folder name from s3 bucket folder path

    Args:
        prefix (str): Folder path

    Returns:
        str: Folder name from a given path
    """
    (abs_path, _) = os.path.split(prefix)
    dir = os.path.basename(abs_path)
    return dir


def list_objects(prefix: str):
    """Retrieves a list of s3 objects in a given folder

    Args:
        prefix (str): Folder path

    Returns:
        list: List of s3 objects
    """
    response = client.list_objects_v2(
        Bucket=config.BUCKET,
        Prefix=prefix,
        Delimiter="/",
    )
    objects = []
    if "Contents" in response:
        objects = [obj["Key"] for obj in response["Contents"]]
    return objects


def extract_s3_objects(date: datetime):
    """Constructs prefix from a given datetime object to retrieve s3 objects
    Args:
        date (datetime): Datetime for construct sub folder path

    Returns:
        list: List of s3 objects for a given datetime object
    """
    print("Extracting file patterns ", config.PATTERN, " for given date: ", date.date())
    prefix = (
        config.PREFIX
        + str(date.year)
        + "/"
        + str(date.month).zfill(2)
        + "/"
        + str(date.day).zfill(2)
        + "/"
    )
    objects = list_objects(prefix)
    return objects


def extract_filenames_with_pattern(date: datetime):
    """
    Filters filenames based on the grid patterns passed
    Args:
        date (datetime): Datetime for filename

    Returns:
        list: List of filtered grid filenames
    """
    objects = extract_s3_objects(date)
    filtered_list = []

    if len(objects) <= 0:
        print("Files not found for given date: ", date.date())
        prev_day = date - timedelta(days=1)
        if date.day < calendar.monthrange(date.year, date.month)[1]:
            next_day = date + timedelta(days=1)
            print("Extracting files for next date: ", next_day.date())
            objects = extract_s3_objects(next_day)
            if len(objects) <= 0:
                print("Files not found for next available date: ", next_day.date())
                objects = extract_s3_objects(prev_day)
        else:
            print("Extracting files for previous date: ", prev_day.date())
            objects = extract_s3_objects(prev_day)

    for pat in config.PATTERN:
        matched = [os.path.basename(obj).split(".")[0] for obj in objects if pat in obj]
        filtered_list.extend(matched)
    print(
        "Found files ",
        filtered_list,
        " with pattern ",
        config.PATTERN,
        " for given date: ",
        date.date(),
    )
    return filtered_list


def export_to_csv(data: list, year: int = None, month: int = None):
    """
    Export filenames to a csv file for analysis. If year and month are supplied
    filenams are appended to csv file otherwise headers are appended at the beginnign of the file.

    Args:
        data (list): List of filenames
        year (int, optional): Year to which filenames belongs to. Defaults to None.
        month (int, optional): Month to which filenames belongs to. Defaults to None.
    """
    if len(data) > 0:
        mode = "w" if not year else "a"
        with open("filenames.csv", mode, newline="") as file:
            writer = csv.writer(file)
            if not year:
                writer.writerow(data)
            else:
                yyyymm = f"{year}{str(month).zfill(2)}"
                writer.writerow([yyyymm])
                for filename in data:
                    writer.writerow([filename])


def every_fifth_day_of_every_month_in_a_year(year: int):
    """
    Calculates every 5th day of every month in a year.
    This helps in constructing prefixes for every 5 days.

    Args:
        year (int): Year on which 5 day periods are calculated
    """

    # Retrieves monthly prefixes from S3 bucket for a given year
    monthly_prefixes = prefix_list(config.PREFIX + str(year) + "/")

    # Retrieves list of months from the prefixes
    months = [int(folder_path(prefix)) for prefix in monthly_prefixes]

    for month in months:
        filenames = []
        for day in config.DAYS:
            try:
                # Calculate every fifthe day of the month
                current_date = datetime(year, month, day)
            except ValueError:
                # Handles fifth day for the month of February
                last_day = calendar.monthrange(year, month)
                current_date = datetime(year, month, last_day[1])
            extracted = extract_filenames_with_pattern(current_date)
            filenames.extend(extracted)
        print(f"Exporting data for yyyymm: {year}{month}")
        export_to_csv(filenames, year, month)


def execute():
    """
    Starts the script to retrieve grid filenames for sudan flood analysis
    """
    # Add CSV headers to the file
    export_to_csv(["Filenames"])
    yearly_prefixes = prefix_list(config.PREFIX)
    for prefix in yearly_prefixes:
        year = int(folder_path(prefix))
        every_fifth_day_of_every_month_in_a_year(year)


if __name__ == "__main__":
    execute()
