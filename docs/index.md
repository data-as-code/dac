# `dac`: Data as Code

<div align="center">
  <img src="img/motto.png" alt="drawing" width="450"/>
</div>

Data-as-Code (DaC) `dac` is a tool that supports the distribution of data as (python) code.

<div align="center">
  <img src="img/logo.jpg" alt="drawing" width="250"/>
</div>

## How will the Data Scientists use a DaC package?

Say that the Data Engineers prepared the `demo-data` as code for you. Then you will install the code in your environment
```sh
python -m pip install demo-data
```
and then you will be able to access the data simply with
```python
from demo_data import load

data = load()
```

Data can be in any format. There is no constraint of any kind.

Not only accessing data will be this easy but, depending on how data were prepared, you may also have access to useful metadata. How?
```python
from demo_data import Schema
```

With the schema you could, for example

* access the column names (e.g. `Schema.my_column`)
* unit test your functions by getting a data example with `Schema.example()`

## How can a Data Engineer provide a DaC python package?

Install this library
```sh
python -m pip install dac
```
and use the command `dac pack` (run `dac pack --help` for detailed instructions).

On a high level, the most important elements you must provide are:

* python code to load the data
* a `Schema` class that at very least contains a `validate` method, but possibly also

    - data field names (column names, if data is tabular)
    - an `example` method

* python dependencies

!!! hint "Use `pandera` to define the Schema"

    If the data type you are using is supported by [`pandera`](https://pandera.readthedocs.io/en/stable/index.html) consider  using a [`DataFrameModel`](https://pandera.readthedocs.io/en/stable/dataframe_models.html) to define the Schema.


## What are the advantages of distributing data in this way?

* The code needed to load the data, the data source, and locations are abstracted away from the user.
  This mean that the data engineer can start from local files, transition to SQL database, cloud file storage, or kafka topic, without having the user to notice it or need to adapt its code.

* *If you provide data field names in `Schema`* (e.g. `Schema.column_1`), the user code will not contain hard-coded column names, and changes in data source field names won't impact the user.

* *If you provide the `Schema.example` method*, users will be able to build robust code by writing unit testing for their functions effortlessly.

* Semantic versioning can be used to communicate significant changes:

  * a patch update corresponds to a fix in the data: its intended content is unchanged
  * a minor update corresponds to a change in the data that does not break the schema
  * a major update corresponds to a change in the schema, or any other breaking change

  In this way data pipelines can subscribe to the appropriate updates. Furthermore, it will be easy to keep releasing data updates maintaining retro-compatibility (one can keep deploying `1.X.Y` updates even after version `2` has been rolled-out).

* Description of the data and columns can be included in the schema, and will therefore reach the user together with the data.

* Users will always know where to look for data: the PyPi index.
