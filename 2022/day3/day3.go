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
	msg := "something went wrong!"
	panic(msg)
}

func findOverlap3(s1 string, s2 string, s3 string) string {
	for i := range s1 {
		s := s1[i : i+1]
		if len(s) != 1 {
			panic("slicing error")
		}
		if strings.Contains(s2, s) && strings.Contains(s3, s) {
			return s
		}
	}
	panic("no overlap found")
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

func part2(filename string) int {
	priority := strings.Split("0abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", "")
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	total := 0
	var inputs [3]string
	i := 0
	for scanner.Scan() {
		// fmt.Println(runningTotal)
		inputs[i] = scanner.Text()
		i++
		if i == 3 {
			overlap := findOverlap3(inputs[0], inputs[1], inputs[2])
			total += indexOf(priority, overlap)
			i = 0
		}
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
	answer = part2("sample.txt")
	if answer != 70 {
		fmt.Println(answer)
		panic("wrong answer to sample problem, part2")
	}
	fmt.Println(part2("input.txt"))
}
