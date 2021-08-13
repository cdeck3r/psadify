# naming package the same as module is bad style
# https://stackoverflow.com/a/60913263
from psadify import psadify
import argparse

from psadify import __version__
from psadify import __author__
from psadify import __email__


def main():
    logo_msg = '\n PSADify v' + __version__ + ' by ' + __author__ + ' (' +__email__+')'

    epilog_msg = ('example:\n' +
                 ' $ python psadify.py -output status.html\n' +
                 logo_msg + '\n A tool for converting PSAD output into HTML.')

    parser = argparse.ArgumentParser(add_help=False,formatter_class=argparse.RawTextHelpFormatter,epilog=epilog_msg)
    parser.add_argument('-h', '--help', dest='show_help', action='store_true', help='Show this message and exit\n\n')
    parser.add_argument('-o', '--output', help='The file that is generated with the HTML content\n', type=str)
    parser.set_defaults(show_help='False')
    args = parser.parse_args()

    if args.show_help is True:
        print('')
        print(parser.format_help())
        sys.exit(0)

    print(logo_msg)

    output_file = 'status.html'
    if args.output:
        output_file = args.output

    html = psadify.get_html(psadify.get_last_attacks(), psadify.get_top_attackers(), psadify.get_top_signatures(), psadify.get_top_ports())

    with open(output_file, 'w') as f:
        print(' [*] Writing output to ' + output_file)
        f.write(html)

    print('')

