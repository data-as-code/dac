import pandas as pd


class Schema:
    int1 = "int1"
    float1 = "float1"
    string1 = "string1"
    date1 = "date1"
    datetime1 = "datetime1"

    @classmethod
    def validate(cls, check_obj: pd.DataFrame, **kwargs) -> pd.DataFrame:
        # columns are present
        for col in (cls.int1, cls.float1, cls.string1, cls.date1, cls.datetime1):
            assert col in check_obj.columns

        # correct types
        assert check_obj[cls.int1].dtype == int
        assert check_obj[cls.float1].dtype == float
        assert check_obj[cls.string1].dtype == object
        assert check_obj[cls.date1].dtype == object
        assert check_obj[cls.datetime1].dtype == "datetime64[ns]"

        # no nulls in int1
        assert check_obj[cls.int1].isna().sum() == 0

        return check_obj
