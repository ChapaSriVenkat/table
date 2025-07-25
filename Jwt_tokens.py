import jwt
import datetime
import logging

SECRET_KEY = "your_secret_key_here"

logging.basicConfig(filename='backend.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_token(username: str) -> str:
    logging.info(f"Generating token for: {username}")
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "iat": datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def decode_token(token: str):
    try:
        logging.info("Decoding JWT token")
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        logging.warning("Token has expired")
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        logging.error("Invalid token")
        return {"error": "Invalid token"}

