from __future__ import unicode_literals, absolute_import

from operator import methodcaller
from sys import version
from codecs import open

from openedx_modulestore_utils.expand_nested import main as expand_nested_main
from openedx_modulestore_utils.utils import pp, pdata

if version[0] == "2":
    iteritems = methodcaller("iteritems")
else:
    iteritems = methodcaller("items")


def to_filtered_csv(ms, output_fname):
    with open(output_fname, "wt", encoding="utf8") as f:
        f.write("block_id\tcategory\tdisplay_name\texam\n")
        f.write(
            "\n".join(
                "\t".join(
                    '"\\N"' if val is None else '"{}"'.format(val)
                    for val in (
                        k,
                        v["category"],
                        v["metadata"].get("display_name"),
                        v["metadata"].get("exam"),
                    )
                )
                for k, v in iteritems(ms)
            )
        )
        f.write("\n")
    # _metadata(ms)


def _metadata(ms):
    pp({key for k, v in iteritems(ms) for key in v["metadata"]})


def main(output_fname=None):
    output_fname = pdata("ms.csv") if output_fname is None else output_fname
    ms, input_fname, _, _ = expand_nested_main()
    to_filtered_csv(ms, output_fname)


if __name__ == "__main__":
    main()
