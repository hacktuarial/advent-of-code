package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

type elf struct {
	low  int
	high int
}

func isFullyContained(left elf, right elf) bool {
	// left is fully contained in right
	leftInRight := (left.low >= right.low && left.high <= right.high)
	// or, right is fully contained in left
	rightInLeft := (right.low >= left.low && right.high <= left.high)
	return leftInRight || rightInLeft
}

func anyOverlap(left elf, right elf) bool {
	return ((left.low <= right.low && left.high >= right.low) ||
		(right.low <= left.low && right.high >= left.low))
}

func makeElf(str string) elf {
	both := strings.Split(str, "-")
	low, _ := strconv.Atoi(both[0])
	high, _ := strconv.Atoi(both[1])
	return elf{low: low, high: high}
}

func makeElves(str0 string) []elf {
	out := make([]elf, 2)
	str := strings.Split(str0, ",")
	out[0] = makeElf(str[0])
	out[1] = makeElf(str[1])
	return out
}

func part1(filename string) int {
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	total := 0
	for scanner.Scan() {
		txt := scanner.Text()
		elves := makeElves(txt)
		if isFullyContained(elves[0], elves[1]) {
			total++
		}
	}
	return total
}
func part2(filename string) int {
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	total := 0
	for scanner.Scan() {
		txt := scanner.Text()
		elves := makeElves(txt)
		if anyOverlap(elves[0], elves[1]) {
			total++
		}
	}
	return total
}

func main() {
	// part 1
	answer := part1("sample.txt")
	if answer != 2 {
		panic("wrong answer to sample problem, part1")
	}
	fmt.Println(part1("input.txt"))
	// part 2
	answer = part2("sample.txt")
	if answer != 4 {
		panic("wrong answer to sample problem, part2")
	}
	fmt.Println(part2("input.txt"))
}
