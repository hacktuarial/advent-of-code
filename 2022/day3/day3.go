package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"sort"
	"strings"
)

func findOverlap(s1 []string, s2 []string) string {
	i, j := 0, 0
	for i+j < len(s1)+len(s2) {
		if s1[i] < s2[j] {
			i++
		} else if s1[i] == s2[j] {
			return s1[i]
		} else {
			j++
		}
	}
	return "something went wrong!"
}

func indexOf(arr []string, target string) int {
	for i, v := range arr {
		if v == target {
			return i
		}
	}
	return -1
}

func part1(filename string) int {
	priority := strings.Split("0abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", "")
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	total := 0
	var left, right []string
	for scanner.Scan() {
		// fmt.Println(runningTotal)
		txt := scanner.Text()
		midpoint := len(txt) / 2
		left = strings.Split(txt[:midpoint], "")
		right = strings.Split(txt[midpoint:], "")
		sort.Strings(left)
		sort.Strings(right)
		overlap := findOverlap(left, right)
		total += indexOf(priority, overlap)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	return total
}

func main() {
	// part 1
	answer := part1("sample.txt")
	if answer != 157 {
		panic("wrong answer to sample problem, part1")
	}
	fmt.Println(part1("input.txt"))
	// part2
	// answer = part2("sample.txt")
	// if answer != 12 {
	// 	panic("wrong answer to sample problem, part1")
	// }
	// fmt.Println(part2("input.txt"))
}
