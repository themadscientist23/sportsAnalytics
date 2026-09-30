import os

from balldontlie import BalldontlieAPI
from dotenv import load_dotenv

load_dotenv()

api = BalldontlieAPI(api_key=os.environ["BALLDONTLIE_API_KEY"])
