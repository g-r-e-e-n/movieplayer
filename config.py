
import os
import re
from logger import LOGGER
from dotenv import load_dotenv

load_dotenv()

YSTREAM=False
STREAM=os.environ.get("STARTUP_STREAM", "https://idvd.multitvsolution.com/idvo/discoverytamil_540p/index.m3u8")
regex = r"^(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?"
match = re.match(regex,STREAM)
if match:
    YSTREAM=True
    finalurl=STREAM
    LOGGER.warning("YouTube Stream is set as STARTUP STREAM")
else:
    finalurl=STREAM

class Config:
    ADMIN = os.environ.get("AUTH_USERS", "")
    ADMINS = [int(admin) for admin in (ADMIN).split()]
    API_ID = int(os.environ.get("API_ID", ""))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")     
    SESSION = os.environ.get("SESSION_STRING", "")
    BOT_USERNAME=None
    CHAT_ID = int(os.environ.get("CHAT_ID", ""))
    LOG_GROUP=os.environ.get("LOG_GROUP", "")
    if LOG_GROUP:
        LOG_GROUP=int(LOG_GROUP)
    else:
        LOG_GROUP=None
    STREAM_URL=finalurl
    YSTREAM=YSTREAM
    SHUFFLE=bool(os.environ.get("SHUFFLE", True))
    ADMIN_ONLY=os.environ.get("ADMIN_ONLY", "False")
    REPLY_MESSAGE=os.environ.get("REPLY_MESSAGE", None)
    if REPLY_MESSAGE:
        REPLY_MESSAGE=REPLY_MESSAGE
        LOGGER.warning("Reply Message Found, Enabled PM Guard !")
    else:
        REPLY_MESSAGE=None
    EDIT_TITLE = os.environ.get("EDIT_TITLE", True)
    if EDIT_TITLE == "False":
        EDIT_TITLE=None
        LOGGER.warning("VC Title Editing Turned OFF !")
    msg = {}
    playlist=[]
    CONV = {}
    FFMPEG_PROCESSES={}
    GET_FILE={}
    STREAM_END={}
    CALL_STATUS=False
    PAUSE=False
    STREAM_LINK=False
    ADMIN_CACHE=False
