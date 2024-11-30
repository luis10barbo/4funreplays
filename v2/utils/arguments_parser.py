import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='obr')
    parser.add_argument('--new-cfg', action="store_true", help="create new cfg", dest='new_cfg')
    args = parser.parse_args()
    return args
