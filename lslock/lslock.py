"""lslock: prints the PIDs and paths of all files locked beneath a directory
"""
import os
import sys
from prettytable import PrettyTable


LOCKS_FILE = "/proc/locks"


def _parse_locks():
    """Parse /proc/locks and return a list of locks
    :rtype: list
    :return: a list of locks entries, each lock entry is a dict that contains
             the lock properties listed in /proc/locks

    Sample entries in /proc/locks
    1: FLOCK  ADVISORY  WRITE 160 00:1e:4749 0 EOF
    1: -> FLOCK  ADVISORY  WRITE 3914 00:1e:4749 0 EOF
    2: FLOCK  ADVISORY  WRITE 102 00:1e:879 0 EOF

    """
    locks = []
    with open(LOCKS_FILE, "r") as locks_file:
        lines = locks_file.readlines()
    # remove the empty lines
    lines = [l.replace("-> ", "") for l in lines if l.strip()]
    for lock_record in lines:
        specs = [s for s in lock_record.split(" ") if s]
        lock = {"lid": specs[0].replace(":", ""),
                "lclass": specs[1],
                "ltype": specs[2],
                "permission": specs[3],
                "pid": specs[4],
                "fid": specs[5],
                "start_region": specs[6],
                "end_region": specs[7]
                }
        locks.append(lock)
    return locks


def _get_stats(directory):
    """Walk a directory to get all the files and their inodes
    Returns a dict with the file names as keys and inodes as values
    """
    fstats = {}
    for cur, dirs, files in os.walk(directory):
        for fname in files:
            fpath = os.path.join(cur, fname)
            fstats[fpath] = str(os.stat(fpath).st_ino)
    return fstats


def list_locks(directory):
    """Returns the pids and paths of all locked files under a directory
    :param :class:`str` directory: Top level directory to scan for locked files
    :rtype: list
    :return: A list of tuples: (filepath, [pid1, pid2,...])
    """
    locked_files = []
    # get the locked inodes
    locks = _parse_locks()
    # build a dict that has inodes has keys and list of pids as values
    l_inodes = {}
    for f in locks:
        inode = f["fid"].split(':')[2]
        if inode not in l_inodes:
            l_inodes[inode] = []
        l_inodes[inode].append(f["pid"])

    # walk the directory and search each file's inode in l_inodes
    # if file is locked, add the filepath and pids to locked_files
    for cur, dirs, files in os.walk(directory):
        for fname in files:
            fpath = os.path.join(cur, fname)
            inode = str(os.stat(fpath).st_ino)
            if inode in l_inodes.keys():
                locked_files.append((fpath, l_inodes[inode]))
    return locked_files


def main():
    """Usage: lslock <directory>
    """
    def _usage():
        print "{0}: list locked files under a directory".format(sys.argv[0])
        print "Usage: lslock <directory>"
    if len(sys.argv) < 2:
        _usage()
        sys.exit(1)
    directory = sys.argv[1]
    locked_files = list_locks(directory)
    t = PrettyTable(["PID", "PATH"])
    t.border = False
    print "Locked files under {0}:".format(directory)
    for fname, pids in locked_files:
        for pid in pids:
            t.add_row([pid, fname])
    print t


if __name__ == '__main__':
    main()
