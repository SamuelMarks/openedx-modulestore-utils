openedx-modulestore-utils
=========================

Clean utility functions for the [OpenEdX](https://open.edx.org) [modulestore](http://edx.readthedocs.io/projects/edx-developer-guide/en/latest/modulestores/split-mongo.html#split-mongo-modulestore).

## Dependencies

Python 2.7 (nothing external!). Python 3 compatibility trivial to add; just ask if you want it.

## Setup

After `cd`ing to a live edx-platform—and activating the virtualenv—dump your modulestore like so:

    ./manage.py lms --settings aws dump_course_structure course-v1:<org>+<course_id>+<run> > /tmp/ms.json

Now you can use it like so:

    expand_nested(acquire_data('/tmp/ms.json'),
                  metadata=({'display_name': 'Pre-Training Test'},
                            {'display_name': 'Post-Training Test'}),
                  output_fname='/tmp/parsed_ms.json')

Here the metadata I care about is supplied, you probably care about something different; modify accordingly.

Note: this walks the tree from chapter downwards.

---

## MySQL import

Python:

    ms, input_fname, _, _ = expand_nested_main()
    to_filtered_csv(ms, '/tmp/ms.csv')

Then in MySQL:

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
