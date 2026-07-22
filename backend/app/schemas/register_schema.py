from pydantic import BaseModel, EmailStr

class RegisterUser(BaseModel):
    full_name: str
    email: EmailStr
    password: str