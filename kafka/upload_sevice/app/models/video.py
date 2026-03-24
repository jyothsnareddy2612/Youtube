from pydantic import BaseModel

class VideoUploadRequest(BaseModel):
    title: str
    description: str
    file_path: str
    user_id: str