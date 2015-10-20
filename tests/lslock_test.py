"""Tests for lslock
"""
import os
import subprocess
import pytest

from lslock import lslock


TEST_DIR = "/tmp/lslock-test"


def lock_file(filepath):
    """flock a file
    """
    # run flock command to get exclusive lock on a file
    cmd = "flock -x {0} -c cat".format(filepath)
    subprocess.Popen(cmd.split(), stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)


@pytest.fixture
def locked():
    """Create the test files and lock them,
    return a list of locked files
    """
    locked_files = []
    files_to_lock = ["A/A.txt",
                     "A/a/aa/aa.txt",
                     "B/B.txt",
                     "B/b/b.txt"
                     ]
    for fname in files_to_lock:
        fpath = os.path.join(TEST_DIR, fname)
        # create the directory if it doesn't exist
        if not os.path.exists(os.path.dirname(fpath)):
            os.makedirs(os.path.dirname(fpath))
        # create the file if it doesn't exist
        if not os.path.exists(fpath):
            with open(fpath, "w") as f:
                f.write("File {0}".format(fpath))
        lock_file(fpath)
        locked_files.append(fpath)
    return (TEST_DIR, locked_files)


def test_lock_files(locked):
    """Verify lslock program returns correct list of locked files
    """
    test_dir = locked[0]
    lslock_locks = lslock.list_locks(test_dir)
    lslock_locked_files = [l[0] for l in lslock_locks]
    assert(sorted(lslock_locked_files) == sorted(locked[1]))
