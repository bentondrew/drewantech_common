#  Copyright 2016
#  Drewan Tech, LLC
#  ALL RIGHTS RESERVED

from contextlib import contextmanager

login = 'postgresql://{user}:{password}@{host}:{port}/{database}'


def connect_to_database(user_name,
                        user_password,
                        database_host,
                        database_port,
                        database_name):
  from sqlalchemy import create_engine
  from sqlalchemy.pool import NullPool
  engine = create_engine(login.format(user=user_name,
                                      password=user_password,
                                      host=database_host,
                                      port=database_port,
                                      database=database_name),
                         poolclass=NullPool)
  return engine


def execute_postgres_command(engine, command):
  connection = engine.connect()
  connection.execute('COMMIT')
  connection.execute(str(command))
  connection.close()


@contextmanager
def database_transaction(engine):
  from sqlalchemy.orm import sessionmaker
  Session = sessionmaker(bind=engine)
  session = Session()
  try:
    yield session
    session.commit()
  except Exception as e:
    session.rollback()
    raise e
  finally:
    session.close()
