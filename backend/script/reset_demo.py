"""
This script resets the SQLAlchemy database to contain a greater abundance
of data than `test_reset.py` for greater UI testing.

Previously, we duplicated data between testing and this database reset.
Moving forward, we'll aim to have some parity between tests and dev reset.
This way, we both avoid duplication and make it easier to interact with
the state of the system we are writing tests for.

Usage: Start from the root directory python3 -m backend.script.reset_demo
"""

import sys
from sqlalchemy import text
from sqlalchemy.orm import Session
from ..database import engine
from ..env import getenv
from .. import entities

from ..test.services import role_data, user_data, permission_data
from ..test.services.organization import organization_demo_data
from ..test.services.event import event_demo_data

from ..test.services.coworking import room_data, seat_data, operating_hours_data, time
from ..test.services.coworking.reservation import reservation_data

__authors__ = ["Sameera & Dharshini", "Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Ensures that the script can only be run in development mode
if getenv("MODE") != "development":
    print("This script can only be run in development mode.", file=sys.stderr)
    print("Add MODE=development to your .env file in workspace's `backend/` directory")
    exit(1)

# Reset Tables
entities.EntityBase.metadata.drop_all(engine)
entities.EntityBase.metadata.create_all(engine)

# Initialize the SQLAlchemy session
with Session(engine) as session:
    # Load all demo data
    time = time.time_data()
    role_data.insert_fake_data(session)
    user_data.insert_fake_data(session)
    permission_data.insert_fake_data(session)
    organization_demo_data.insert_fake_data(session)
    event_demo_data.insert_fake_data(session)
    operating_hours_data.insert_fake_data(session, time)
    room_data.insert_fake_data(session)
    seat_data.insert_fake_data(session)
    reservation_data.insert_fake_data(session, time)

    # Commit changes to the database
    session.commit()
