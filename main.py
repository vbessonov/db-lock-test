import sys
from datetime import datetime
from multiprocessing import Process

from core import Base, Session, WorkCoverageRecord, engine
from update import process_function, ProcessMode

if __name__ == "__main__":
    process_mode = ProcessMode.DEADLOCK

    if len(sys.argv) == 2:
        process_mode = ProcessMode(int(sys.argv[1]))

    # Drop the test tables and recreate them.
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = Session()

    # Add some test records.
    records = []

    for i in range(10):
        record = WorkCoverageRecord(id=i, timestamp=datetime.utcnow())
        records.append(record)

    session.add_all(records)
    session.commit()

    # Create processes updating the test records simultaneously.
    processes = []

    for i in range(2):
        process = Process(target=process_function, args=(i, process_mode))
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()
