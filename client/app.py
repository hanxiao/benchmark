from math import ceil

import numpy as np
from gnes.cli.parser import set_client_cli_parser
from gnes.client.cli import CLIClient
from gnes.helper import get_duration
from gnes.proto import gnes_pb2
from google.protobuf.json_format import Parse


class MyClient(CLIClient):

    @property
    def bytes_generator(self):
        for _ in range(self.args.num_docs):
            yield b'a' * self.args.num_bytes

    def analyze(self):
        num_effective_lines = ceil(self.args.num_docs / self.args.batch_size)
        summary = {}
        if self.args.test_id:
            with open('/workspace/network%d.json' % self.args.test_id) as fp:
                infos = [Parse(v, gnes_pb2.Envelope()).routes for v in fp.readlines()[-num_effective_lines:]]
                summary['f:send interval'] = [get_duration(infos[j][0].start_time, infos[j + 1][0].start_time) for j in
                                              range(len(infos) - 1)]
                summary['f:recv interval'] = [get_duration(infos[j][0].end_time, infos[j + 1][0].end_time) for j in
                                              range(len(infos) - 1)]
                summary['f->r1 trans'] = [get_duration(j[0].start_time, j[1].start_time) for j in infos]
                summary['r1->r2 trans'] = [get_duration(j[1].end_time, j[2].start_time) for j in infos]
                summary['r2->f trans'] = [get_duration(j[2].end_time, j[0].end_time) for j in infos]
                summary['roundtrip'] = [get_duration(j[0].start_time, j[0].end_time) for j in infos]

        print('%40s\t%6s\t%6s\t%6s\t%6s\t%6s' % ('measure', 'mean', 'std', 'median', 'max', 'min'))
        for k, v in summary.items():
            print('%40s\t%3.3fs (+-%2.2f)\t%3.3fs\t%3.3fs\t%3.3fs' % (
                k, np.mean(v), np.std(v), np.median(v), np.max(v), np.min(v)))


if __name__ == '__main__':
    parser = set_client_cli_parser()
    parser.add_argument('--num_bytes', type=int, default=10,
                        help='number of bytes per doc')
    parser.add_argument('--num_docs', type=int, default=10,
                        help='number of docs in total')
    parser.add_argument('--test_id', type=int,
                        help='test id')
    parser.add_argument('--override_benchmark', action='store_true', default=False,
                        help='override previous benchmark json data')
    args = parser.parse_args()
    m = MyClient(args)
    m.analyze()
