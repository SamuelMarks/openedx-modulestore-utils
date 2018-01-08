from os import path
from json import load, dump
from pprint import PrettyPrinter
from copy import deepcopy

from utils import update_d, set_update_d

pp = PrettyPrinter(indent=4).pprint


def acquire_data(fname=None):
    with open(path.join(path.dirname(__file__), '_data', 'modulestore.json') if fname is None else fname, 'rt') as f:
        data = load(f)
    return data


def give_children_top_metadata(ms, parsed_blocks, block_id, top_metadata):
    block = parsed_blocks[block_id]

    if 'children' not in block:
        return block

    for child in block['children']:
        current_block_id = child.keys()[0]
        set_update_d(child, 'metadata', top_metadata)
        ms[current_block_id]['metadata'].update(deepcopy(top_metadata))
        give_children_top_metadata(ms, child, current_block_id, top_metadata)


def expand_nested(ms, metadata=None, output_fname=None):
    chapters = {k: unwrap_block(ms, k) for k, v in ms.iteritems()
                if v['category'] == 'chapter' and (metadata is None or v['metadata'] in metadata)}

    for chapter_name in chapters:
        give_children_top_metadata(ms, chapters[chapter_name],
                                   chapter_name, chapters[chapter_name].values()[0]['metadata'])

    if output_fname:
        with open(output_fname, 'wt') as f:
            dump(ms, f, indent=4, sort_keys=True)
    return chapters


def unwrap_block(ms, block_id):
    current_block = deepcopy(ms[block_id])
    return {block_id: update_d(current_block,
                               {'children': [unwrap_block(ms, child)
                                             for child in current_block['children']]}
                               if 'children' in current_block else {})}


if __name__ == '__main__':
    expand_nested(acquire_data(),
                  metadata=({'display_name': 'Pre-Training Test'},
                            {'display_name': 'Post-Training Test'}),
                  output_fname=path.join(path.dirname(__file__), '_data', 'ms.json'))
