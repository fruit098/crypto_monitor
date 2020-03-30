from .database import commit_session, init_connection

_, SESSION, BASE_MODEL = init_connection(
    "postgresql://postgres:docker@localhost:5432/postgres"
)

__all__ = ("BASE_MODEL", "SESSION", "commit_session")
