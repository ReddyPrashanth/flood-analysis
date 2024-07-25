# S3 Bucket
BUCKET = "noaa-jpss"

# Base path prefix for s3 bucket where data is available
PREFIX = "JPSS_Blended_Products/VFM_5day_GLB/ShapeZIP/"

# Grid patterns to filter objects from the bucket list
PATTERN = ["GLB085", "GLB086"]

# list of every nth days in a month
DAYS = [5, 10, 15, 20, 25, 30]


AWS_ACCESS_KEY_ID = None
AWS_SECRET_ACCESS_KEY = None
