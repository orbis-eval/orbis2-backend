from typing import Optional, Dict

from pydantic import BaseModel, Field


class ResponseModel(BaseModel):
    status_code: int = Field(..., description='Status of response', enum=[200, 201, 400, 401])
    message: str = Field(..., description='Error Message if request could not be processed')
    content: Optional[Dict]

    class Config:
        schema_extra = {
            "example":
                {
                    "status_code": 200,
                    "message": "",
                    "content": {"some_key": "some_value"}
                }
        }
