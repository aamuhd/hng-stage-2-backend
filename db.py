from sqlmodel import create_engine



sqlite_filename = 'my_db.db'
sqlite_url = f'sqlite:///./{sqlite_filename}'

engine = create_engine(
    sqlite_url,
    connect_args={'check_same_thread': False},
)