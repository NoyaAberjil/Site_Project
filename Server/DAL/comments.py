from bunnet import Document
# from bson import ObjectId
from datetime import datetime

class Comments(Document):
    Recipe_ID: str
    userName: str
    comment: str  
    dop: datetime

    def validate_comment(self) -> tuple[bool, str]:
        """בדיקה שהתגובה תקינה"""
        if not self.comment or len(self.comment.strip()) < 1:
            return False, "התגובה חייבת להכיל לפחות תו אחד"
        return True, ""
    


