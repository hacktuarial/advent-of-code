from typing import List, Dict
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.DEBUG)


@dataclass
class File:
    size: int
    name: str  # not needed

    def __repr__(self):
        return f"{self.name} (file, size={self.size})"


@dataclass
class Directory:
    name: str
    parent: "Directory"
    files: List[File]
    children: Dict

    def size(self):
        return sum(file.size for file in self.files) + sum(
            child.size() for child in self.children.values()
        )

    def addFile(self, file):
        self.files.append(file)

    def addChild(self, name, directory):
        if name in self.children:
            raise ValueError(f"{name} already present")
        self.children[name] = directory

    def __repr__(self):
        output = "\n"
        for file in self.files:
            output += f"{file}\n"
        for child in self.children.values():
            output += f"{child}\n"
        return output


def parse_input(instructions):
    root = Directory(name="/", parent=None, files=[], children={})
    node = root
    i = 1
    while i < len(instructions):
        line = instructions[i]
        assert line.startswith("$")
        # could be cd or ls
        if "ls" in line.split():
            # ls: add files and children to node
            i += 1
            line = instructions[i]
            while not line.startswith("$"):
                if line.startswith("dir"):
                    # add a directory to node
                    name = line.split()[-1]
                    directory = Directory(name=name, files=[], children={}, parent=node)
                    logging.debug("adding a child directory %s to %s", name, node.name)
                    node.addChild(
                        name=name,
                        directory=directory,
                    )
                else:
                    # add a file to node
                    size, name = line.split()
                    file = File(size=int(size), name=name)
                    logging.debug("adding a file %s to %s", file, node.name)
                    node.addFile(file)
                # go on to the next line
                i += 1
                try:
                    line = instructions[i]
                except IndexError:
                    # reached end of file
                    break
        else:
            # cd: change node
            target = line.split()[-1]
            if target == "..":
                node = node.parent
            else:
                # change into a subdirectory
                logging.debug("Moving into %s", node.name + "/" + target)
                node = node.children[target]
            i += 1
    return root


def add_up_sizes(directory, threshold=100_000):
    size = directory.size()
    if size > threshold:
        size = 0
    return size + sum(
        add_up_sizes(child, threshold) for child in directory.children.values()
    )


if __name__ == "__main__":
    fname = "sample.txt"  # sys.argv[1]
    with open(fname, "r") as f:
        instructions = f.readlines()
    root = parse_input(instructions)
    assert root.size() == 48381165
    assert root.children["d"].size() == 24933642
    assert root.children["a"].children["e"].size() == 584
    assert root.children["a"].size() == 94853
    total_size = add_up_sizes(root, 100_000)
    assert total_size == 95437, total_size

    # part 1
    fname = "input.txt"
    with open(fname, "r") as f:
        instructions = f.readlines()
    root = parse_input(instructions)
    print(add_up_sizes(root, 100_000))
