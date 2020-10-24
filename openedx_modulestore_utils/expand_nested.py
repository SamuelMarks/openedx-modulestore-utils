from __future__ import unicode_literals, absolute_import

from codecs import getwriter, open
from json import load, dump
from copy import deepcopy
from operator import methodcaller
from sys import version

from openedx_modulestore_utils.utils import update_d, set_update_d, pdata

if version[0] == "2":
    iteritems = methodcaller("iteritems")
else:
    iteritems = methodcaller("items")


def acquire_data(fname):
    with open(fname, "rt", encoding="utf8") as f:
        data = load(f, encoding="utf8")
    return data


def give_children_top_metadata(ms, parsed_blocks, block_id, top_metadata):
    block = parsed_blocks[block_id]

    if "children" not in block:
        return block

    for child in block["children"]:
        current_block_id = child.keys()[0]
        set_update_d(child, "metadata", top_metadata)
        ms[current_block_id]["metadata"].update(deepcopy(top_metadata))
        give_children_top_metadata(ms, child, current_block_id, top_metadata)


def expand_nested(ms, metadata=None, output_fname=None):
    chapters = {
        k: unwrap_block(ms, k)
        for k, v in iteritems(ms)
        if v["category"] == "chapter"
        and (metadata is None or v["metadata"] in metadata)
    }

    for chapter_name in chapters:
        chapter = chapters[chapter_name].values()[0]
        top_metadata = deepcopy(chapter["metadata"])
        top_metadata["exam"] = top_metadata.pop("display_name")
        ms[chapter_name]["metadata"]["exam"] = chapter["metadata"][
            "exam"
        ] = top_metadata["exam"]
        give_children_top_metadata(
            ms, chapters[chapter_name], chapter_name, top_metadata
        )

    if output_fname:
        with open(output_fname, "wt", encoding="utf8") as f:
            dump(
                ms, getwriter("utf-8")(f), ensure_ascii=False, sort_keys=True, indent=4
            )
    return chapters


def unwrap_block(ms, block_id):
    current_block = deepcopy(ms[block_id])
    return {
        block_id: update_d(
            current_block,
            {
                "children": [
                    unwrap_block(ms, child) for child in current_block["children"]
                ]
            }
            if "children" in current_block
            else {},
        )
    }


def main(input_fname=None, output_fname=None, metadata=None):
    output_fname = pdata("ms.json") if output_fname is None else output_fname
    ms = acquire_data(pdata("modulestore.json") if input_fname is None else input_fname)
    return (
        ms,
        input_fname,
        output_fname,
        expand_nested(
            ms,
            metadata=(
                {"display_name": "Pre-Training Test"},
                {"display_name": "Post-Training Test"},
            )
            if metadata is None
            else metadata,
            output_fname=output_fname,
        ),
    )


if __name__ == "__main__":
    main()
