import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='obr')
    parser.add_argument("--record", action="store_true", help="record replay", dest='record')
    parser.add_argument("--thumbnail", action="store_true", help="create thumbnail", dest='thumbnail')
    parser.add_argument("--description", action="store_true", help="create description", dest='description')
    parser.add_argument('--new-cfg', action="store_true", help="create new cfg", dest='new_cfg')
    parser.add_argument('--dl-maps', action="store_true", help="download maps", dest='dl_maps')

    args = parser.parse_args()
    return args
