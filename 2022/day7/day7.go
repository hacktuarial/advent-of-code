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
	return strings.Split(line, " ")[1] == "cd"
}
func isLS(line string) bool {
	return strings.Split(line, " ")[1] == "ls"
}

func day7(filename string) int {
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	var root Directory
	var currentDir *Directory
	root = Directory{name: "/", parent: nil, children: make([]Directory, 0), files: 0}
	currentDir = &root
	lines := make([]string, 0)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	// fmt.Println(strings.Join(lines, "\n")) . // same as input
	// skip the first one, which just does cd into /
	var i = 1
	for i = 1; i < len(lines); i++ {
		// fmt.Println("current line is `" + lines[i] + "`")
		if isCommand(lines[i]) {
			if isCD(lines[i]) {
				destination := strings.Split(lines[i], " ")[2]
				if destination == ".." {
					fmt.Println(currentDir.name)
					currentDir = currentDir.parent
				} else {
					for _, child := range currentDir.children {
						if child.name == destination {
							currentDir = &child
							break
						}
					}
					panic("could not find subdirectory " + destination + " of parent " + currentDir.name)
				}

			} else if isLS(lines[i]) {
				// Need to look at the next lines
				for i = i + 1; !isCommand(lines[i]); i++ {
					if isDirectory(lines[i]) {
						child := Directory{name: strings.Split(lines[i], " ")[1],
							parent: currentDir, children: make([]Directory, 0),
							files: 0}
						currentDir.addChild(child)
						fmt.Println("I added directory " + child.name + " to " + currentDir.name)
					} else {
						// it's a file
						fileName := strings.Split(lines[i], " ")[1]
						fileSize, _ := strconv.Atoi(strings.Split(lines[i], " ")[0])
						currentDir.addFile(fileSize)
						fmt.Println("I added file " + fileName + " to " + currentDir.name)
					}
				}

			} else {
				panic("Unknown command" + lines[i])
			}

		} else {
			panic("don't know what to do with this: " + lines[i])
		}
	}
	return 0
}

func main() {
	// part 1
	// fmt.Println("the answer to part1 is ")
	fmt.Println(day7("sample.txt"))
	// part 2
	// fmt.Println("the answer to part2 is ")
	// fmt.Println(day6("input.txt", 14))
	// if answer != "MCD" {
	// 	panic("wrong answer to sample problem, part2")
	// }
	// fmt.Println("the answer to part2 is " + day5("input.txt", false, false))
}
