import pandas as pd

# when using docker in docker (DinD), the following path must be used
DIND_DATAFOLDER = '/workspace/benchmark/'


# DIND_DATAFOLDER = ''

def load(id):
    if id == 0:
        with open(DIND_DATAFOLDER + '.github/README-template.md') as fp:
            return [fp.read()]
    else:
        with open(DIND_DATAFOLDER + '.github/%d.md' % id) as fp:
            c_md = fp.read()

        bh = pd.read_json(DIND_DATAFOLDER + '.data/history%d.json' % id, lines=True)
        bh = bh.sort_values(by=['timestamp_build'])

        return [c_md, bh.to_html(
            index=False,
            escape=False,
            border=0,
            bold_rows=False,
            columns=['version_vcs',
                     'roundtrip',
                     'MB/s',
                     'f:send',
                     'f:recv',
                     'f->r1:send',
                     'r1->r2:send',
                     'r2->f:send',
                     'timestamp_build',
                     'timestamp_eval',
                     'version_tag', ],
            float_format='{:4.3f}'.format,
            formatters={
                'version_vcs': lambda x: '<a href="GURL/%s"><code>%s</code></a>' % (x, x),
                'version_tag': lambda x: '<code>%s</code>' % x,
            }).replace('GURL', 'https://github.com/gnes-ai/gnes/commit')]


results = [v for j in range(5) for v in load(j)]

with open(DIND_DATAFOLDER + 'README.md', 'w', encoding='utf8') as fp:
    fp.write('\n\n'.join(results))
