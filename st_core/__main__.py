import os
from os.path import expanduser
import argparse

if __name__ == '__main__':
    home_dir = expanduser("~")
    cur_dir  = os.getcwd()

    print home_dir,cur_dir

    parser = argparse.ArgumentParser(description='1.Description',
    epilog='2.Epilog',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('args',nargs="*",type=str,help="args help",default=['12'])

    parser.add_argument('-f',"--foo",nargs="?",type=int,default=42,help='foo help')
    parser.add_argument('-g',action='store_true')
    args = parser.parse_args()

    print "args:",args
    print "args.foo:",args.foo

    quit()
