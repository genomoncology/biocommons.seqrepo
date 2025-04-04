import os
import shutil
import tempfile

import pytest

from biocommons.seqrepo.fastadir.fabgz import FabgzReader, FabgzWriter

seed = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
sequences = {"l{l}".format(l=l): seed * l for l in (1, 10, 100, 1000, 10000)}


def test_write_reread():
    # PY2BAGGAGE: Switch to TemporaryDirectory
    tmpdir = tempfile.mkdtemp(prefix="seqrepo_pytest_")

    fabgz_fn = os.path.join(tmpdir, "test.fa.bgz")

    # write sequences
    faw = FabgzWriter(fabgz_fn)
    for seq_id, seq in sequences.items():
        faw.store(seq_id, seq)
    # add twice to demonstrate non-redundancy
    for seq_id, seq in sequences.items():
        faw.store(seq_id, seq)
    faw.close()

    # now read them back
    far = FabgzReader(fabgz_fn)
    assert far.filename.startswith(tmpdir.encode())  # type: ignore
    assert far.fetch("l1") == seed * 1
    assert far.fetch("l10") == seed * 10
    assert far.fetch("l100") == seed * 100
    assert far.fetch("l1000") == seed * 1000
    assert far.fetch("l10000") == seed * 10000

    shutil.rmtree(tmpdir)


def test_errors():
    with pytest.raises(RuntimeError):
        far = FabgzWriter("/tmp/badsuffix")


if __name__ == "__main__":
    test_write_reread()
