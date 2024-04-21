"""SQL Database"""

import struct

from azure.identity import DefaultAzureCredential
from sqlalchemy import Engine, event
from sqlalchemy.engine import URL
from sqlmodel import Session, create_engine

SQL_COPT_SS_ACCESS_TOKEN = 1256  # As defined in msodbcsql.h


sql_engine: Engine | None = None


def inject_azure_credential(
    credential, engine, token_url="https://database.windows.net/.default"
):
    @event.listens_for(engine, "do_connect")
    def do_connect(dialect, conn_rec, cargs, cparams):
        token = credential.get_token(token_url).token.encode("utf-16-le")
        token_struct = struct.pack(f"=I{len(token)}s", len(token), token)
        cargs[0] = cargs[0].replace(";Trusted_Connection=Yes", "")
        attrs_before = cparams.setdefault("attrs_before", {})
        attrs_before[SQL_COPT_SS_ACCESS_TOKEN] = bytes(token_struct)

        return dialect.connect(*cargs, **cparams)


def create_sql_engine():
    global sql_engine

    if sql_engine:
        return sql_engine

    connection_url = URL.create(
        "mssql+pyodbc",
        host="ic-ent-e2-cwjsl-sql-dev.database.windows.net",
        database="cwjsl",
        query={"driver": "ODBC Driver 18 for SQL Server"},
    )

    sql_engine = create_engine(connection_url)

    default_azure_credential = DefaultAzureCredential()

    inject_azure_credential(default_azure_credential, sql_engine)

    return sql_engine


class SQLSession:
    def __call__(self):
        sql_engine = create_sql_engine()

        session = Session(sql_engine)
        try:
            yield session
        finally:
            session.close()
