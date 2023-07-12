package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

type Directory struct {
	name     string
	parent   *Directory
	children []*Directory
	files    int
}

func (dir Directory) sizes() []int {
	sizes := make([]int, 1)
	sizes[0] = dir.size()
	for _, child := range dir.children {
		for _, size := range child.sizes() {
			sizes = append(sizes, size)
		}
	}
	return sizes
}

func (dir Directory) size() int {
	size := dir.files
	for _, child := range dir.children {
		size += child.size()
	}
	return size
}

func (dir *Directory) addChild(child *Directory) {
	dir.children = append(dir.children, child)
}

func (dir *Directory) addFile(filesize int) {
	dir.files += filesize
}

func isCommand(line string) bool {
	return line[0:1] == "$"
}

func isDirectory(line string) bool {
	return line[:3] == "dir"
}

func isCD(line string) bool {
	return line[:4] == "$ cd"
}

func isLS(line string) bool {
	return line[:4] == "$ ls"
}

func day7(filename string) int {
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	var root Directory
	var currentDir *Directory // currentDir is a pointer
	root = Directory{name: "/", parent: nil, children: make([]*Directory, 0), files: 0}
	currentDir = &root
	lines := make([]string, 0)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	// fmt.Println(strings.Join(lines, "\n")) . // same as input
	// skip the first one, which just does cd into /
	var i int
	for i = 1; i < len(lines); i++ {
		fmt.Println("current working directory is `" + currentDir.name + "`")
		if isCD(lines[i]) {
			destination := strings.Split(lines[i], " ")[2]
			fmt.Println("I want to change working directory to " + destination)
			if destination == ".." {
				currentDir = currentDir.parent
			} else {
				for _, child := range currentDir.children {
					if child.name == destination {
						currentDir = child
						fmt.Println("I changed working directory to " + currentDir.name)
						break
					} else {
						fmt.Println(child.name + " != " + destination)
					}
				}
				// msg := "could not find subdirectory " + destination + " of parent " + currentDir.name + ". Its children are ("
				// for _, child := range currentDir.children {
				// 	msg += child.name + ","
				// }
				// msg += ")"
				// panic(msg)

			}

		} else if isLS(lines[i]) {
			// Need to look at the next lines
			for i = i + 1; i < len(lines) && !isCommand(lines[i]); i++ {
				if isDirectory(lines[i]) {
					child := Directory{name: strings.Split(lines[i], " ")[1],
						parent: currentDir, children: make([]*Directory, 0),
						files: 0}
					currentDir.addChild(&child)
					fmt.Println("I added directory " + child.name + " to " + currentDir.name)
				} else {
					// it's a file
					oldSize := int64(currentDir.files)
					fileName := strings.Split(lines[i], " ")[1]
					fileSize, _ := strconv.Atoi(strings.Split(lines[i], " ")[0])
					currentDir.addFile(fileSize)
					newSize := int64(currentDir.files)
					fmt.Println("I added file " + fileName + " to " + currentDir.name)
					fmt.Println("its size increased from " + strconv.FormatInt(oldSize, 10) +
						" to " + strconv.FormatInt(newSize, 10))
				}
			}
			// fmt.Println("I broke out of the ls loop. i=" + strconv.FormatInt(int64(i), 10))
			i--

		} else {
			panic("Unknown command" + lines[i])
		}

	}
	sizes := root.sizes()
	total := 0
	for _, size := range sizes {
		if size < 100000 {
			total += size
		}
	}
	return total
}

func main() {
	// part 1
	if day7("sample.txt") != 95437 {
		panic("wrong answer to sample")
	}
	fmt.Println("the answer to part1 is ")
	fmt.Println(day7("input.txt"))
	// part 2
	// fmt.Println("the answer to part2 is ")
	// fmt.Println(day6("input.txt", 14))
	// if answer != "MCD" {
	// 	panic("wrong answer to sample problem, part2")
	// }
	// fmt.Println("the answer to part2 is " + day5("input.txt", false, false))
}
