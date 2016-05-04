#  Copyright 2016
#  Drewan Tech, LLC
#  ALL RIGHTS RESERVED


from contextlib import contextmanager


class PostgresqlDatabaseManipulation(object):
  """For creating, connecting to and deleting Postgresql databases.

  Attributes:
    db_user (str): Database user name with database creation and dropping
      permissions.

    db_password (str): Database password associated with database user.

    db_host (str): Database host name.

    db_port (int): Port to communicate with database.

    default_db (str): Name of user default database for logging in to create
      or drop databases.

  Raises:
    ValueError: If provided attributes are not of the correct type.

  """
  def __init__(self, db_user, db_password, db_host, db_port, default_db):
    self.login = 'postgresql://{user}:{password}@{host}:{port}/{database}'
    if type(db_user) is not str:
      raise ValueError('The db_user arg passed in the '
                       'PostgresqlDatabaseManipulation initialization is not '
                       'a str type.')
    if type(db_password) is not str:
      raise ValueError('The db_password arg passed in the '
                       'PostgresqlDatabaseManipulation initialization is not '
                       'a str type.')
    if type(db_host) is not str:
      raise ValueError('The db_host arg passed in the '
                       'PostgresqlDatabaseManipulation initialization is not '
                       'a str type.')
    if type(db_port) is not int:
      raise ValueError('The db_port arg passed in the '
                       'PostgresqlDatabaseManipulation initialization is not '
                       'an int type.')
    if type(default_db) is not str:
      raise ValueError('The default_db arg passed in the '
                       'PostgresqlDatabaseManipulation initialization is not '
                       'a str type.')
    self.db_credentials = {'user': db_user,
                           'password': db_password,
                           'host': db_host,
                           'port': db_port}
    self.default_db = default_db

  def manipulate_database(self, action, database_name):
    if type(action) is not str:
      raise ValueError('The action arg passed to '
                       'PostgresqlDatabaseManipulation'
                       '.manipulate_database'
                       'function is not a str type.')
    if type(database_name) is not str:
      raise ValueError('The database_name arg passed to '
                       'PostgresqlDatabaseManipulation'
                       '.manipulate_database'
                       'function is not a str type.')
    accepted_database_actions = ['CREATE', 'DROP']
    invalid_databases = ['postgres', self.default_db]
    if action not in accepted_database_actions:
      generated_action_list = ''
      for accepted_action in accepted_database_actions:
        generated_action_list += '{}, '.format(accepted_action)
      generated_action_list = generated_action_list.rstrip(', ')
      raise ValueError('The action arg, {}, passed to '
                       'PostgresqlDatabaseManipulation'
                       '.manipulate_database'
                       'function is not an accepted action. '
                       'The following actions are accepted: {}'
                       .format(action, generated_action_list))
    if database_name in invalid_databases:
      raise ValueError('The database_name, {}, passed to '
                       'PostgresqlDatabaseManipulation '
                       '.manipulate_database '
                       'function cannot be acted on with this '
                       'class.'.format(database_name))
    command = '{} DATABASE {}'.format(action, database_name)
    self.execute_default_database_command(command=command)

  def execute_default_database_command(self, command):
    if type(command) is not str:
      raise ValueError('The command, {}, passed to '
                       'PostgresqlDatabaseManipulation'
                       '.execute_default_database_command '
                       'function is not a str type.'.format(command))
    engine = self.connect_to_database(self.default_db)
    connection = engine.connect()
    connection.execute('COMMIT')
    connection.execute(command)
    connection.close()

  def connect_to_database(self, database_name):
    if type(database_name) is not str:
      raise ValueError('The database_name arg passed to '
                       'PostgresqlDatabaseManipulation'
                       '.connect_to_database'
                       'function is not a str type.')
    from sqlalchemy import create_engine
    from sqlalchemy.pool import NullPool
    engine = create_engine(self.login.format(database=database_name,
                                             **self.db_credentials),
                           poolclass=NullPool)
    return engine


@contextmanager
def database_transaction(engine):
  from sqlalchemy.engine import Engine
  from sqlalchemy.orm import sessionmaker
  if type(engine) is not Engine:
    raise ValueError('The engine provided to '
                     'database_operations.database_transaction function is '
                     'not a sqlalchemy Engine type.')
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


if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser('Test the module for creating and '
                                   'dropping postgresql databases.')
  parser.add_argument('action',
                      choices=['CREATE', 'DROP'],
                      help='Action to take with database.')
  args = parser.parse_args()
  db_connection = PostgresqlDatabaseManipulation('benton',
                                                 'benton',
                                                 'localhost',
                                                 5432,
                                                 'benton')
  db_connection.manipulate_database(args.action, 'test')
