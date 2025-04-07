from datetime import date, datetime

import pandera as pa
from pandera.typing import Series


class Schema(pa.DataFrameModel):
    int1: Series[int] = pa.Field(nullable=False)
    float1: Series[float] = pa.Field()
    string1: Series[str] = pa.Field()
    date1: Series[date] = pa.Field()
    datetime1: Series[datetime] = pa.Field()
