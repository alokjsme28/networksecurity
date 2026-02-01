import logging
import os
from datetime import datetime

# Log file name
Log_File = f"{datetime.now().strftime('%d-%m-%Y_%H_%M_%S')}.log"

# Path to store the logs
log_path = os.path.join(os.getcwd(),'logs')

#Make directory
os.makedirs(log_path,exist_ok=True)

# Actual Log File Path
Log_File_Path = os.path.join(log_path,Log_File)

#Configure logging
logging.basicConfig(
    filename=Log_File_Path,
    level=logging.INFO,
    format = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s"
)



