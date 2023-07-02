package main

import (
    "bufio"
    "fmt"
    "log"
    "os"
	"strconv"
	"sort"
)

func makeArray(k int) []int {
	// return [k]int; this doesn't work!
	return make([]int, k)
}

func day1(filename string, topK int) int {
    file, err := os.Open(filename)
    if err != nil {
        log.Fatal(err)
    }
    defer file.Close()

    scanner := bufio.NewScanner(file)
	var max = makeArray(topK)
	runningTotal := 0
    for scanner.Scan() {
		// fmt.Println(runningTotal)
        txt := scanner.Text()
		if (txt == "") {
			if (runningTotal > max[0]) {
				max[0] = runningTotal
				// not sure why I need a slice here
				sort.Ints(max[:])	
			}	
			runningTotal = 0
		} else {
			intVar, _ := strconv.Atoi(txt)
			runningTotal += intVar
		}
    }

    if err := scanner.Err(); err != nil {
        log.Fatal(err)
    }
	total := 0
	for _, v := range max {
		total += v
	}
	return total
}

func main() {
	// part 1
	answer := day1("sample.txt", 1)
	if (answer != 24000) {
		panic("wrong answer to sample problem, part1")
	}
	fmt.Println(day1("input.txt", 1))
	// part 2
	answer = day1("sample.txt", 3)
	if (answer != 45000) {
		panic("wrong answer to sample problem, part2")
	}
	fmt.Println(day1("input.txt", 3))
}