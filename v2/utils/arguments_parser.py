import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='obr')
    parser.add_argument('--new-cfg', action="store_true", help="create new cfg", dest='new_cfg')
    parser.add_argument('--dl-maps', action="store_true", help="download maps", dest='dl_maps')

    args = parser.parse_args()
    return args
