iport pandera as pa
from pandera.typing import Series


class Schema(pa.SchemaModel):
    A: Series[int] = pa.Field(nullable=False)
    B: Series[float] = pa.Field(nullable=False)
