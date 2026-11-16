import os
from dotenv import load_dotenv

load_dotenv(override=True)

print("HOST:", repr(os.getenv("DB_HOST")))
print("USER:", repr(os.getenv("DB_USER")))
print("PORT:", repr(os.getenv("DB_PORT")))
print("DATABASE:", repr(os.getenv("DB_NAME")))
print("SENHA CONFIGURADA:", bool(os.getenv("DB_PASSWORD")))