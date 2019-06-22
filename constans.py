import os


FIXTURES_PATH = 'tests/fixtures'
MODELS = 'service_api/domain/models'

API_PREFIX = 'chats'
DB_NAME = os.getenv('DB_NAME')

# SMS settings
send_sms_path = 'http://api.myatompark.com/members/sms/xml.php'
send_sms_header = {"Content-type": "application/x-www-form-urlencoded"}

login = os.getenv('ePOCHTA_LOGIN')
password = os.getenv('ePOCHTA_PASSWORD')
public_key = os.getenv('ePOCHTA_PUB_KEY')
msg_id = "123456"
