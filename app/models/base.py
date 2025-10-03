import random
import string
from datetime import datetime

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy.orm import relationship

from app.db.session import Base


def gen_id():
    """Generate a simple random string ID"""
    ran = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    return str(ran)


__all__ = ["Base", "gen_id", "Column", "String", "Integer", "Float", "Boolean", 
           "DateTime", "ForeignKey", "JSON", "Text", "BLOB", "relationship", "datetime"]
