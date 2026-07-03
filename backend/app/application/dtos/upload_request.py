from pydantic import BaseModel


class UploadRequest(BaseModel):
    """DTO for the upload request."""

    # When uploading files via multipart/form-data, FastAPI typically 
    # handles the File object. This DTO is more for future expansiveness 
    # if extra JSON metadata is sent alongside the file.
    pass
