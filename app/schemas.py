from pydantic import BaseModel, EmailStr


class CheckInRequest(BaseModel):
    email: EmailStr
    name: str | None = None
    phone: str | None = None
    send_email: bool = True


class CheckInResponse(BaseModel):
    success: bool
    message: str
    is_new_user: bool
    email_sent: bool


class UserResponse(BaseModel):
    id: str
    email: str
    name: str | None
    phone: str | None
    tags: list[str]
