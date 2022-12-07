from typing import List, Dict
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.DEBUG)


@dataclass
class File:
    size: int
    name: str  # not needed


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


def parse_input(instructions):
    root = Directory(name="/", parent=None, files=[], children={})
    node = root
    i = 1
    while i < len(instructions):
        line = instructions[i]
        is_command = line.startswith("$")
        if is_command:
            # could be cd or ls
            if "ls" in line.split():
                # ls: add files and children to node
                i += 1
                line = instructions[i]
                logging.debug(line)
                while not line.startswith("$"):
                    if line.startswith("dir"):
                        name = line.split()[-1]
                        directory = Directory(
                            name=name, files=[], children={}, parent=node
                        )
                        logging.debug("Adding a child directory %s", directory)
                        node.addChild(
                            name=name,
                            directory=directory,
                        )
                    else:
                        size, name = line.split()
                        file = File(size=int(size), name=name)
                        logging.debug("adding a file %s", file)
                        node.addFile(file)
                    i += 1
                    line = instructions[i]

            else:
                # cd: change node
                target = line.split()[-1]
                if target == "..":
                    node = node.parent
                else:
                    # change into a subdirectory
                    logging.debug("Moving into %s", node.name + "/" + target)
                    try:
                        node = node.children[target]
                    except KeyError as e:
                        raise ValueError(line)
            i += 1
            line = instructions[i]
                            

    return root


def add_up_sizes(directory, running_total, threshold=100_000):
    if directory.size() <= threshold:
        running_total += directory.size()
    for child in directory.children.values():
        running_total += add_up_sizes(child, running_total, threshold)
    return running_total


if __name__ == "__main__":
    fname = "sample.txt"  # sys.argv[1]
    logging.debug(fname)
    with open(fname, "r") as f:
        instructions = f.readlines()
    root = parse_input(instructions)
    total_size = add_up_sizes(root, 0, 100_000)
    print(total_size)
