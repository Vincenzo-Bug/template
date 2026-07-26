"""SQLAlchemy foundation tests."""

from app.infrastructure.database import Base


def test_metadata_uses_deterministic_constraint_names() -> None:
    """Alembic must receive stable naming conventions."""
    convention = Base.metadata.naming_convention

    assert convention is not None
    assert convention["pk"] == "pk_%(table_name)s"
    assert convention["fk"] == (
        "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
    )
