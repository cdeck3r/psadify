# naming package the same as module is bad style
# https://stackoverflow.com/a/60913263
import argparse
import errno
import os
import sys

from psadify import __author__, __email__, __version__, psadify


def check_log_files(PSAD_LOG_DIR='/var/log/psad'):
    """Check for required logfiles in log directory

    Check for
    - /var/log/psad/top_attackers
    - /var/log/psad/top_sigs
    - /var/log/psad/top_ports

    It will exist, if one of the logfiles does not exist.

    Parameters:
    PSAD_LOG_DIR -- the logfile directory (default: '/var/log/psad')

    """
    log_files = ['top_attackers', 'top_sigs', 'top_ports']
    for f in log_files:
        psad_log_file = os.path.join(PSAD_LOG_DIR, f)
        if not os.path.isfile(psad_log_file):
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), psad_log_file
            )
    return True


def main():
    PSAD_LOG_DIR = '/var/log/psad'

    logo_msg = (
        '\n PSADify v' + __version__ + ' by ' + __author__ + ' (' + __email__ + ')'
    )

    epilog_msg = (
        'example:\n'
        + ' $ python psadify.py -output status.html\n'
        + logo_msg
        + '\n A tool for converting PSAD output into HTML.'
    )

    parser = argparse.ArgumentParser(
        add_help=False, formatter_class=argparse.RawTextHelpFormatter, epilog=epilog_msg
    )
    parser.add_argument(
        '-h',
        '--help',
        dest='show_help',
        action='store_true',
        help='Show this message and exit\n\n',
    )
    # option --filter-private-ip
    # removes NetName: PRIVATE-ADDRESS-CBLK-RFC1918-IANA-RESERVED from psadify report
    # default: enable
    parser.add_argument(
        '-x',
        '--filterprivateip',
        help='Filters private IPs from psadify report. DEFAULT: enable\n',
        nargs='?',
        type=str,
        choices={'enable', 'disable'},
        const='enable',
        default='enable',
    )
    parser.add_argument(
        '-o',
        '--output',
        help='The file that is generated with the HTML content\n',
        type=str,
    )

    parser.set_defaults(show_help='False')
    args = parser.parse_args()

    if args.show_help is True:
        print('')
        print(parser.format_help())
        sys.exit(0)

    print(logo_msg)

    # default: enable / filter_private_ip=True
    filter_private_ip = True if (args.filterprivateip == 'enable') else False

    output_file = 'status.html'
    if args.output:
        output_file = args.output

    # exists with an OSError, if a required logfile does not exist
    check_log_files(PSAD_LOG_DIR)

    html = psadify.get_html(
        psadify.get_last_attacks(),
        psadify.get_top_attackers(),
        psadify.get_top_signatures(),
        psadify.get_top_ports(),
    )

    with open(output_file, 'w') as f:
        print(' [*] Writing output to ' + output_file)
        f.write(html)

    print('')
