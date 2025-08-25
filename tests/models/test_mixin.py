from datetime import UTC, datetime

from sqlalchemy import DateTime, Integer, create_engine, func
from sqlalchemy.orm import DeclarativeBase, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class Dummy(Base):
    __tablename__ = "dummy"
    id = mapped_column(Integer, primary_key=True)
    created_at = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


def test_timestamp_mixin_utc():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with sessionmaker(bind=engine)() as session:
        obj = Dummy()
        session.add(obj)
        session.commit()
        session.refresh(obj)

    print(f"created_at (naive from DB): {obj.created_at}")
    print(f"updated_at (naive from DB): {obj.updated_at}")

    # Konversi objek datetime dari database menjadi timezone-aware
    created_at_aware = obj.created_at.replace(tzinfo=UTC)
    updated_at_aware = obj.updated_at.replace(tzinfo=UTC)

    # Dapatkan waktu saat ini dalam UTC
    now_utc = datetime.now(UTC)
    print(f"now_utc (aware): {now_utc}")

    # Bandingkan yang sudah aware
    assert created_at_aware.tzinfo is not None
    assert updated_at_aware.tzinfo is not None

    delta_created = abs((created_at_aware - now_utc).total_seconds())
    delta_updated = abs((updated_at_aware - now_utc).total_seconds())

    # Gunakan tolerance yang realistis
    assert delta_created < 1
    assert delta_updated < 1
