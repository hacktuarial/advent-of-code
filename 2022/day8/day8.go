package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func visibleFromLeft(X [][]int, row int, col int) bool {
	// always visible from edge
	if row*col == 0 {
		return true
	}
	for j := col - 1; j >= 0; j-- {
		if X[row][j] >= X[row][col] {
			return false
		}
	}
	return true
}
func visibleFromRight(X [][]int, row int, col int) bool {
	for j := col + 1; j < len(X); j++ {
		if X[row][j] >= X[row][col] {
			return false
		}
	}
	return true
}
func visibleFromTop(X [][]int, row int, col int) bool {
	for i := 0; i < row; i++ {
		if X[i][col] >= X[row][col] {
			return false
		}
	}
	return true
}
func visibleFromBottom(X [][]int, row int, col int) bool {
	for i := row + 1; i < len(X); i++ {
		if X[i][col] >= X[row][col] {
			return false
		}
	}
	return true
}

func isVisible(X [][]int, row int, col int) int {
	if visibleFromBottom(X, row, col) || visibleFromLeft(X, row, col) || visibleFromTop(X, row, col) || visibleFromRight(X, row, col) {
		return 1
	} else {
		return 0
	}
}

func countLeft(X [][]int, row int, col int) int {
	var k int
	for k = 1; col-k > 0 && X[row][col-k] < X[row][col]; k++ {
	}
	return k
}

func countRight(X [][]int, row int, col int) int {
	var k int
	for k = 1; col+k < len(X)-1 && X[row][col+k] < X[row][col]; k++ {
	}
	return k
}

func countUp(X [][]int, row int, col int) int {
	var k int
	for k = 1; row-k > 0 && X[row-k][col] < X[row][col]; k++ {
	}
	return k
}

func countDown(X [][]int, row int, col int) int {
	var k int
	for k = 1; row+k < len(X)-1 && X[row+k][col] < X[row][col]; k++ {
	}
	return k
}

func scenicScore(X [][]int, row int, col int) int {
	left := countLeft(X, row, col)
	right := countRight(X, row, col)
	up := countUp(X, row, col)
	down := countDown(X, row, col)
	fmt.Println(row, col, left, up, right, down)
	return up * left * right * down
}

func totalVisible(X [][]int) int {
	total := 0
	N := len(X[0])
	for i := 0; i < N; i++ {
		for j := 0; j < N; j++ {
			total += isVisible(X, i, j)
		}
	}
	return total
}

func buildMatrix(filename string) [][]int {
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	matrix := make([][]int, 0)
	for scanner.Scan() {
		txt := strings.Split(scanner.Text(), "")
		row := make([]int, len(txt))
		for i, val := range txt {
			row[i], _ = strconv.Atoi(val)
		}
		matrix = append(matrix, row)
	}
	return matrix
}

func part1(filename string) int {
	matrix := buildMatrix(filename)
	return totalVisible(matrix)
}

func part2(filename string) int {
	matrix := buildMatrix(filename)
	maxScenicScore := -1
	for row := 1; row < len(matrix)-1; row++ {
		for col := 1; col < len(matrix)-1; col++ {
			score := scenicScore(matrix, row, col)
			if score > maxScenicScore {
				maxScenicScore = score
			}
		}

	}
	return maxScenicScore
}

func main() {
	var answer int
	answer = part1("sample.txt")
	if answer != 21 {
		panic("wrong answer to sample problem")
	}
	fmt.Println("the answer to part 1 is ")
	fmt.Println(part1("input.txt"))

	answer = part2("sample.txt")
	fmt.Println(answer)
	fmt.Println("the answer to part 2 is ")
	fmt.Println(part2("input.txt"))
}
