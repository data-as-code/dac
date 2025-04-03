iport pandera as pa # noqa: E999
from pandera.typing import Series


class Schema(pa.DataFrameModel):
    A: Series[int] = pa.Field(nullable=False)
    B: Series[float] = pa.Field(nullable=False)
