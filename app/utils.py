# Import Libraries
from passlib.context import CryptContext

# For password protection and hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

# Generate a simple hash method for all password protection
def hash(password: str):
    return pwd_context.hash(password)

# Create a function for hashing a login attempt password and verifying to a stored password
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)