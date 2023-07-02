package day2

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
)


// rock, paper, scissors

func getPosition(arr []string, target string) int {
	for i, v := range arr {
		if (v == target) {
			return i
		}
	}
	return -1
}

func absValue(x int) int {
	if (x > 0) {
		return x
	} else {
		return -x
	}
}

func play(self int, opponent int) int {
	// -1 lose, 0 draw, 1 win
	diff := self - opponent
	if (diff == 0) {
		return 0
	} else if absValue(diff) == 1 {
		return -diff
	} else {
		return -1
	}
}


func score(opponent string, self string) int {
	// rock, paper, scissors
	SELF := [4]string{"0", "A", "B", "C"}
	OPPONENT := [4]string{"0", "X", "Y", "Z"}
	selfInt := getPosition(SELF[:], self)
	oppInt := getPosition(OPPONENT[:], opponent)
	if (selfInt == oppInt) {
		// draw
		return 3 + selfInt;
	} else if (selfInt < oppInt) {
		// lose
		return selfInt;
	} else {
		// win
		return 6 + selfInt;
	}


}

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
		if txt == "" {
			if runningTotal > max[0] {
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
	if answer != 24000 {
		panic("wrong answer to sample problem, part1")
	}
	fmt.Println(day1("input.txt", 1))
	// part 2
	answer = day1("sample.txt", 3)
	if answer != 45000 {
		panic("wrong answer to sample problem, part2")
	}
	fmt.Println(day1("input.txt", 3))
}
