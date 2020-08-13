from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

config = {
    "insta_pass": os.getenv("INSTA_PASS"),
    "insta_mail": os.getenv("INSTA_MAIL"),
    "insta_name": os.getenv("INSTA_NAME"),
    "rd_client": os.getenv("RD_CLIENT_ID"),
    "rd_secret": os.getenv("RD_SECRET"),
    "rd_name": os.getenv("RD_NAME"),
    "rd_dev_name": os.getenv("RD_DEV_NAME"),
    "rd_dev_pass": os.getenv("RD_DEV_PASS")
}
