import sys
import random
import hashlib

############## Problem 2 ##############


class LeafNode:
    def __init__(self, path, hash, file):
        self.path = path
        self.hash = hash
        self.file = file

    def __str__(self):
        return "node={}, hash={}, file={}".format(self.path, self.hash, self.file)


class HashNode:
    def __init__(self, path, hash, left, right):
        self.path = path
        self.hash = hash
        self.left = left
        self.right = right

    def __str__(self):
        return "path={}, hash={}".format(self.path, self.hash)


class MerkleTree:
    def __init__(self):
        self.n = 0

    def _sha256(self, s):
        m = hashlib.sha256()
        m.update(str(s))
        return m.hexdigest()

    def create_tree(self, file_list):
        self.file_list = file_list

        hashes = []
        for i, f in enumerate(file_list):
            fileNode = LeafNode([i], self._sha256(f), f)
            hashes.append(fileNode)

        while len(hashes) > 1:
            next_hashes = []
            for i in range(0, len(hashes), 2):
                A = hashes[i]
                B = hashes[i + 1]
                next_hash = HashNode(
                    A.path + B.path, self._sha256(A.hash + B.hash), A, B)
                next_hashes.append(next_hash)
            hashes = next_hashes

        if len(hashes) != 1:
            raise "Problem constructing the tree."
        self.root = hashes[0]
        return self.root

    def read_file(self, i):
        siblings_list = []
        curr = self.root

        while not isinstance(curr, LeafNode):
            left = curr.left
            right = curr.right
            if i in left.path:
                siblings_list = [(True, right.hash)] + siblings_list
                curr = left
            elif i in right.path:
                siblings_list = [(False, left.hash)] + siblings_list
                curr = right
            else:
                raise 'Cannot find target.'

        return (curr.file, siblings_list)

    def write_file(self, i, file):
        # you esentially have to recompute the entire tree anyway, so let's make
        # life a little bit easier and just use our constructor
        file_list = self.file_list
        file_list[i] = file
        new_root = self.create_tree(file_list)

        return new_root

    def check_integrity(self, i, file, siblings_list):
        computed_hash = self._sha256(file)

        while len(siblings_list) > 0:
            left, twin = siblings_list[0]

            if not left:
                computed_hash = self._sha256(twin + computed_hash)
            else:
                computed_hash = self._sha256(computed_hash + twin)

            siblings_list = siblings_list[1:]

        return computed_hash == self.root.hash


# some code to validate the functionality of our MerkleTree
if len(sys.argv) > 1 and sys.argv[1] == '2.1':
    mt = MerkleTree()
    mt.n = 2**10

    file_list = [i * 30 for i in range(mt.n)]
    root = mt.create_tree(file_list)

    # read 10 valid files
    for i in range(10):
        pos = random.randint(0, mt.n - 1)
        file, siblings_list = mt.read_file(pos)
        valid = mt.check_integrity(pos, file, siblings_list)
        assert file == file_list[pos] and valid

    # read 10 invalid files
    for i in range(10):
        pos = random.randint(0, mt.n - 1)
        file, siblings_list = mt.read_file(pos)
        file = random.randint(0, 1000)
        valid = mt.check_integrity(pos, file, siblings_list)
        assert not valid

    # write 10 files
    for i in range(10):
        pos = random.randint(0, mt.n - 1)
        new_file = random.randint(0, 1000)
        file_list[pos] = new_file
        mt.write_file(pos, new_file)

    # Now run our experiment one more time.
    # read 10 valid files
    for i in range(10):
        pos = random.randint(0, mt.n - 1)
        file, siblings_list = mt.read_file(pos)
        valid = mt.check_integrity(pos, file, siblings_list)
        assert file == file_list[pos] and valid

    # read 10 invalid files
    for i in range(10):
        pos = random.randint(0, mt.n - 1)
        file, siblings_list = mt.read_file(pos)
        file = random.randint(0, 1000)
        valid = mt.check_integrity(pos, file, siblings_list)
        assert not valid

    print 'All MerkleTree tests successful.'
