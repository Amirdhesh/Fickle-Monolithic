from datetime import timedelta,datetime
import jwt
import bcrypt
from pytz import timezone
from uuid import UUID
from app.core.settings import settings



async def create_token(id : UUID , email : str):
    ist = timezone("Asia/kolkata")
    expiry = datetime.now(ist) + timedelta(hours= settings.JWT_EXPIRY_TIME)
    payload= {"id" : str(id),"email":email,"exp" : expiry}
    token = jwt.encode(payload,settings.JWT_SECRET_KEY,settings.JWT_ALGORITHM)
    return token


async def decode_token(token : str):
    try : 
        payload = jwt.decode(token,settings.JWT_SECRET_KEY,settings.JWT_ALGORITHM)
        return payload
    except:
        return None
