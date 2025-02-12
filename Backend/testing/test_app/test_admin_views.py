from datetime import datetime, date, time
from unittest.mock import MagicMock, patch
from app import mail
import pytest
from app.models import (
    Organisation,
    Contact,
    Event,
    News,
    Project,
    Publications,
    Author,
    Magazine,
    db
)
