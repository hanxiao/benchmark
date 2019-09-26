import pandas as pd


def load(id):
    if id == 0:
        with open('.github/README-template.md') as fp:
            return [fp.read()]
    else:
        with open('.github/%d.md' % id) as fp:
            c_md = fp.read()

        bh = pd.read_json('.data/history%d.json' % id, lines=True)
        bh = bh.sort_values(by=['timestamp_build'])

        return [c_md, bh.to_html(
            index=False,
            escape=False,
            columns=['version_vcs',
                     'version_tag',
                     'roundtrip',
                     'f:send interval',
                     'f:recv interval',
                     'f->r1 trans',
                     'r1->r2 trans',
                     'r2->f trans',
                     'timestamp_build',
                     'timestamp_eval'],
            float_format='{:4.3f}'.format,
            formatters={
                'version_vcs': lambda x: '<code>gnes-ai/gnes@%s</code>' % x,
                'version_tag': lambda x: '<code>%s</code>' % x,
            })]


results = [v for j in range(5) for v in load(j)]

with open('README.md', 'w', encoding='utf8') as fp:
    fp.write('\n\n'.join(results))