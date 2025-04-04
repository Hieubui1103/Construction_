This process using paid GPT-4-turbo with OpenAI API. The files are retrieved from an Amazon S3 bucket as the images requirement of GPT-vision have to be in urls (Web retrieval)
The code is written in Python and uses the following libraries:
- `openai`: for interacting with the OpenAI API
- `boto3`: for accessing the Amazon S3 bucket
- `pandas`: for data manipulation and analysis
- `openpyxl`: for Excel manipulation and formatting
- `json`: Processing JSON files
These files includes the process from update the files to AWS S3 to retrieved them and run through OpenAI API , which then the results are saved in an Excel file
