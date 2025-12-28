#!/bin/bash
# Script to clean up Python 3.12 dependencies from Lambda directory
# These will be rebuilt by Docker for Python 3.11 during CDK deployment

echo "Cleaning up incompatible Python 3.12 dependencies..."

cd lambda/weather_ingestion

# Remove all installed Python packages
rm -rf boto3/ botocore/ certifi/ charset_normalizer/ dateutil/ idna/ jmespath/
rm -rf numpy/ pandas/ pyarrow/ pytz/ requests/ s3transfer/ tzdata/ urllib3/
rm -rf six.py bin/ numpy.libs/

# Remove dist-info directories
rm -rf *-*.dist-info/
rm -rf *-*.egg-info/

# Remove compiled Python files
find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true
find . -name "*.pyd" -delete 2>/dev/null || true
find . -name "*.so" -delete 2>/dev/null || true

# Keep only source files and requirements.txt
echo "Cleanup complete! Only source files and requirements.txt remain."
echo "Dependencies will be rebuilt for Python 3.11 during CDK deployment."

