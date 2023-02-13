from datetime import datetime

import pandera as pa
from pandera.typing import Series


class Schema(pa.SchemaModel):
    int1: Series[int] = pa.Field(nullable=False)
    float1: Series[int] = pa.Field()
    string1: Series[float] = pa.Field()
    date1: Series[float] = pa.Field()
    datetime1: Series[datetime] = pa.Field()
