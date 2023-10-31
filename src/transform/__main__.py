from config.settings import s
from config.logger import Logger
from transform.data.aggregation import FlightsProcessor
from transform.db.repository import DbRepo

from sqlalchemy.orm import Session

import asyncio

log = Logger.create(__name__)


def app_routine(db: DbRepo):
    with Session(db.engine) as session, session.begin():  # need to sort rows by date before moving this
        FlightsProcessor().summarize_flight_samples(session, db)


async def main():
    log.info('starting transform app')
    db = DbRepo()
    db.upgrade_db()
    while True:
        try:
            app_routine(db)
        except Exception as e:
            log.error(e)
            if s.transform.suppress_errors is False:
                raise e
            log.info('restarting transform app')
        log.info(f'sleeping for {s.transform.wait_between_runs // 60} minutes')
        await asyncio.sleep(s.transform.wait_between_runs)


if __name__ == '__main__':
    asyncio.run(main())