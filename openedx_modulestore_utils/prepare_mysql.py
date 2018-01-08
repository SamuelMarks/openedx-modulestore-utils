from __future__ import unicode_literals

from io import open

from expand_nested import main as expand_nested_main
from utils import pp, pdata


def to_filtered_csv(ms, output_fname):
    with open(output_fname, 'wt', encoding='utf8') as f:
        f.write('block_id\tcategory\tdisplay_name\texam\n')
        f.write('\n'.join('\t'.join('"\\N"' if val is None else '"{}"'.format(val)
                                    for val in (k, v['category'], v['metadata'].get('display_name'),
                                                v['metadata'].get('exam')))
                          for k, v in ms.iteritems()))
        f.write('\n')
    # _metadata(ms)


def _metadata(ms):
    pp({
        key
        for k, v in ms.iteritems()
        for key in v['metadata']
    })


def main(output_fname=None):
    output_fname = pdata('ms.csv') if output_fname is None else output_fname
    ms, input_fname, _, _ = expand_nested_main()
    to_filtered_csv(ms, output_fname)


if __name__ == '__main__':
    main()
