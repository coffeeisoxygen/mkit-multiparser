from pydantic import Field
from pydantic_settings import BaseSettings


class ConfigDatabase(BaseSettings):
    """Konfigurasi database untuk aplikasi."""

    url: str = "sqlite+aiosqlite:///./mkitparser.db"
    echo: bool = Field(
        False, description="Aktifkan logging SQL. Nonaktifkan untuk produksi."
    )

    timeout: int = Field(5, description="Waktu tunggu (detik) untuk koneksi database.")

    pool_size: int = Field(5, description="Jumlah koneksi yang disimpan dalam pool.")
    max_overflow: int = Field(
        10, description="Jumlah koneksi tambahan yang diizinkan saat pool penuh."
    )
