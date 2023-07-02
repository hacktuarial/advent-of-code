package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

// rock, paper, scissors

func getPosition(arr []string, target string) int {
	for i, v := range arr {
		if v == target {
			return i
		}
	}
	panic("could not find the value")
}

func absValue(x int) int {
	if x > 0 {
		return x
	} else {
		return -x
	}
}

func play(opponent int, self int) int {
	// -1 lose, 0 draw, 1 win
	diff := self - opponent
	if diff == 0 {
		return 0
	} else if absValue(diff) == 1 {
		return diff
	} else {
		if diff < 0 {
			return 1
		} else {
			return -1
		}
	}
}

func score(opponent string, self string) int {
	// rock, paper, scissors
	OPPONENT := [4]string{"0", "A", "B", "C"}
	SELF := [4]string{"0", "X", "Y", "Z"}
	selfInt := getPosition(SELF[:], self)
	oppInt := getPosition(OPPONENT[:], opponent)
	gameOutcome := play(oppInt, selfInt)
	if gameOutcome == 0 {
		// draw
		return 3 + selfInt
	} else if gameOutcome < 0 {
		// lose
		return 0 + selfInt
	} else {
		// win
		return 6 + selfInt
	}
}

func day2(filename string, topK int) int {
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	totalScore := 0
	for scanner.Scan() {
		// fmt.Println(runningTotal)
		txt := scanner.Text()
		arr := strings.Split(txt, " ")
		totalScore += score(arr[0], arr[1])
		// fmt.Println(totalScore)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	return totalScore
}

func main() {
	// part 1
	answer := day2("sample.txt", 1)
	if answer != 15 {
		panic("wrong answer to sample problem, part1")
	}
	fmt.Println(day2("input.txt", 1))
}
