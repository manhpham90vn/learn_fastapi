from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from .database import getDatabase
from .utils import get_current_user

dbDepends = Annotated[Session, Depends(getDatabase)]
userDepends = Annotated[dict, Depends(get_current_user)]
