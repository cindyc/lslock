"""lslock: prints the PIDs and paths of all files locked beneath a directory
"""
import os
import sys


LOCKS_FILE = "/proc/locks"


def parse_locks(): 
    """Parse /proc/locks and return a list of locks
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


def get_stats(directory): 
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
    """Returns the PIDs and paths of all files locked under a directory
    """
    locked_files = []
    # get the locked inodes
    locks = parse_locks()
    # build a dict that has inodes has keys and list of PIDs as values
    l_inodes = {}
    for f in locks: 
        inode = f["fid"].split(':')[2]
        if inode not in l_inodes: 
            l_inodes[inode] = []
        l_inodes[inode].append(f["pid"])

    # get all inodes under the directory
    fstats = get_stats(directory)
    for f_path, f_inode in fstats.iteritems():
        if f_inode in l_inodes.keys(): 
            locked_files.append((f_path, l_inodes[f_inode]))
    return locked_files


if __name__ == '__main__': 
    if len(sys.argv) < 2: 
        print "Directory name is required"
        sys.exit(1)
    dirname = sys.argv[1]
    locked_files = list_locks(dirname)
    print "Locked files under {0}:\nPID\t\tPATH".format(dirname)
    for fname, pids in locked_files: 
        print "{0}\t\t{1}".format(",".join(pids), fname)
