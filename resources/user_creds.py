import os
from dotenv import load_dotenv
load_dotenv()
class SuperAdminCreds:
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")