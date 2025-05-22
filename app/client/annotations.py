from typing import Annotated

from fastapi import Depends

from app.client import models, selectors

CurrentClient = Annotated[models.Client, Depends(selectors.get_current_client)]
