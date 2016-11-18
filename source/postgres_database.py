#  Copyright 2016
#  Drewan Tech, LLC
#  ALL RIGHTS RESERVED

from contextlib import contextmanager

login = 'postgresql://{user}:{password}/{database}'
database_base_command = '{action} DATABASE {database_name}'


def connect_to_database(user_name, user_password, database_name):
  from sqlalchemy import create_engine
  from sqlalchemy.pool import NullPool
  engine = create_engine(login.format(user=user_name,
                                      password=user_password,
                                      database=database_name),
                         poolclass=NullPool)
  return engine


def execute_postgres_command(engine, command):
  connection = engine.connect()
  connection.execute('COMMIT')
  connection.execute(str(command))
  connection.close()


def generate_create_database_command(database_to_create):
  command = database_base_command.format(action='CREATE',
                                         database_name=database_to_create)
  return command


def generate_drop_database_command(database_to_drop):
  command = database_base_command.format(action='DROP',
                                         database_name=database_to_drop)
  return command


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
