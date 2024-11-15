from .base import Base
from sqlalchemy import Date, Text
from sqlalchemy.orm import Mapped, mapped_column


class Sale(Base):
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    report: Mapped[Text] = mapped_column(Text, nullable=True)
