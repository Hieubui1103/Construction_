This process using paid GPT-4o with OpenAI API. The files are embedded with base64 and then passed into chatGPT-4o API for vision tasks.
The code is written in Python and uses the following libraries:
- `openai`: for interacting with the OpenAI API
- `pandas`: for data manipulation and analysis
- `openpyxl`: for Excel manipulation and formatting
These files includes the process from update the files to AWS S3 to retrieved them and run through OpenAI API , which then the results are saved in an Excel file
