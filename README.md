openedx-modulestore-utils
=========================
![Python version range](https://img.shields.io/badge/python-2.7%20|%203-blue.svg)
[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech)
[![License](https://img.shields.io/badge/license-Apache--2.0%20OR%20MIT-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Clean utility functions for the [Open edX](https://open.edx.org) [modulestore](http://edx.readthedocs.io/projects/edx-developer-guide/en/latest/modulestores/split-mongo.html#split-mongo-modulestore).

## Dependencies

No external dependencies (except `pip install pyyaml`; which will be auto-acquired on install).

## Setup

After `cd`ing to a live edx-platform—and activating the virtualenv—dump your modulestore like so:

    ./manage.py lms --settings aws dump_course_structure course-v1:<org>+<course_id>+<run> > /tmp/ms.json

Now you can use it like so:
```python
from openedx_modulestore_utils.expand_nested import acquire_data, expand_nested

expand_nested(
    acquire_data("/tmp/ms.json"),
    metadata=(
        {"display_name": "Pre-Training Test"},
        {"display_name": "Post-Training Test"},
    ),
    output_fname="/tmp/parsed_ms.json",
)
```

Here the metadata I care about is supplied, you probably care about something different; modify accordingly.

Note: this walks the tree from chapter downwards.

---

## MySQL import

Python:
```python
from openedx_modulestore_utils.prepare_mysql import expand_nested_main, to_filtered_csv

ms, input_fname, _, _ = expand_nested_main()
to_filtered_csv(ms, "/tmp/ms.csv")
```

Then in MySQL:
```sql
CREATE TABLE parsed_ms (
  block_id varchar(100) NOT NULL PRIMARY KEY,
  category varchar(20) NOT NULL,
  display_name varchar(20),
  exam varchar(20),
  INDEX(category), INDEX(exam)
) DEFAULT CHARSET=utf8;

LOAD DATA LOCAL INFILE '/tmp/ms.csv' INTO TABLE parsed_ms
FIELDS TERMINATED BY '\t'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(block_id, category, display_name, exam);
```
