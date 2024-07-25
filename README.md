## Sudan Flood Analysis File Extraction

### Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configiration)
- [Example](#example)
- [Requirements](#requirements)
- [Outputs](#outputs)

## Installation

To run this script, ensure you have Python installed on your machine. You will also need to install the boto3 library if you haven't already.

1. Install Python: [Download and install Python](https://www.python.org/downloads/).
2. Creating a python virtual environment on Windows

   ```
   > python -m venv analysis

   > analysis\Scripts\activate
   ```

   OR

3. Creating a python virtual environment on Linux

   ```
   > python -m venv analysis

   > source analysis/bin/activate
   ```

4. Install boto3: Install the boto3 and other dependencies using pip.

   ```
   > pip install -r requirements.txt
   ```

## Usage

1. AWS Credentials: Ensure your AWS credentials are configured properly. You can configure them by setting below config variables in config.py file.

   ```
   > AWS_ACCESS_KEY_ID='YOUR_ACCESS_KEY'

   > AWS_SECRET_ACCESS_KEY='YOUR_SECRET_KEY'
   ```

2. Running the Script: Use the following command to run the script.

   ```
   > python main.py
   ```

## Configiration

1. set below config variables in **config.py** file

   ```
    BUCKET = 'BUCKET_NAME'

    PREFIX = 'BUCKET_PREFIX'

    PATTERN = ['GRID_FORMAT_1', 'GRID_FORMAT_2']
   ```

## EXAMPLE

Here is an example of how to use the script:

```
> analysis\Scripts\activate (activates python venv)

> python main.py
```

## Requirements

- Python 3.11
- Python virtual environment
- boto3 library
- AWS ACCESS_KEY and SECRET_KEY for the S3 bucket

## Outputs

1. Python script generates two outputs files listed below.

   ```
      1. filenames.csv
      2. missing_filenames.csv
   ```

2. **filenames.csv** contains list of filenames for every 5 days in a month every year from noaa-jpss bucket.

3. **missing_filenames.csv** contains list of missing dates where data is not available and list available filenames for each month so that it is useful to find out exact dates missing and can be useful for manually corrections.
