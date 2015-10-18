"""A test program for lslock
"""
import os
import fcntl
import subprocess
from lslock import lslock

test_dir = "/tmp/lslock-test"

files_to_lock = ["A/A.txt", "A/a/aa/aa.txt", "B/B.txt", "B/b/b.txt"]


def setUp(): 
    """Create the test files and lock them
    """
    for fname in files_to_lock: 
        fpath = os.path.join(test_dir, fname)
	if not os.path.exists(os.path.dirname(fpath)): 
            os.makedirs(os.path.dirname(fpath))
        # create the file
        with open(fpath, "w") as f: 
            f.write("Test file {}".format(fpath))
        subprocess.call(["flock", "-x", "-n", filepath, "ls"])


def test_lock_files(): 
    """Verify lslock program retuns locked files
    """
    locked = lslock.list_locks(test_dir)
    locked_files = [lock[0] for lock in locked]
    assert(locked_files == [os.path.join(test_dir, f) for f in files_to_lock])
