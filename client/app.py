from gnes.cli.parser import set_client_cli_parser
from gnes.client.cli import CLIClient


class MyClient(CLIClient):

    @property
    def bytes_generator(self):
        for _ in range(self.args.num_docs):
            yield b'a' * self.args.num_bytes


if __name__ == '__main__':
    parser = set_client_cli_parser()
    parser.add_argument('--num_bytes', type=int, default=10,
                        help='number of bytes per doc')
    parser.add_argument('--num_docs', type=int, default=10,
                        help='number of docs in total')
    MyClient(parser.parse_args())
