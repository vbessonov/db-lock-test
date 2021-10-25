from datetime import datetime
from enum import Enum

from core import Session, WorkCoverageRecord


class ProcessMode(Enum):
    DEADLOCK = 1
    NO_DEADLOCK = 2


def process_function(process_id, mode=ProcessMode.NO_DEADLOCK):
    print(f"Process # {process_id} started")

    session = Session()
    transaction = session.begin()

    if mode == ProcessMode.DEADLOCK:
        # If we sort records in reverse order, it'll guarantee the deadlock.
        if process_id % 2 == 0:
            records = session.query(WorkCoverageRecord).all()
        else:
            records = (
                session.query(WorkCoverageRecord)
                .order_by(WorkCoverageRecord.id.desc())
                .all()
            )
    elif mode == ProcessMode.NO_DEADLOCK:
        # To eliminate a deadlock chance, we need to sort rows processed by multiple processes in the same order.
        records = (
            session.query(WorkCoverageRecord)
            .order_by(WorkCoverageRecord.id.desc())
            .all()
        )

    for record in records:
        # We can't use ORM because it's too smart and will try to do batch update and it will never deadlock.
        # record.timestamp = datetime.utcnow()
        session.execute(
            f"UPDATE workcoveragerecords SET timestamp = '{datetime.utcnow()}' WHERE id = {record.id}"
        )

    transaction.commit()

    print(f"Process # {process_id} finished")

    session.commit()
