from pydantic import BaseModel
from datetime import datetime

class EmailBase(BaseModel):
    sender:str
    recipient: str
    subject: str
    send_time:datetime
    esp:str
    name:str
    company_name:str
    template:str



