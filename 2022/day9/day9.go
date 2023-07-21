package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
)

type move struct {
	direction string
	magnitude int
}

type point struct {
	x int
	y int
}

func getMoves(filename string) []move {
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	moves := make([]move, 0)
	for scanner.Scan() {
		txt := strings.Split(scanner.Text(), "")
		mag, _ := strconv.Atoi(txt[1])
		moves = append(moves, move{direction: txt[0], magnitude: mag})
	}
	return moves
}

func addIfNotPresent(visited []point, new point) {
	for _, p := range visited {
		if p.x == new.x && p.y == new.y {
			return
		}
	}
	visited = append(visited, new)
	fmt.Println("tail has visited this many points:")
	fmt.Println(len(visited))
}

func moveRight(p point) point {
	return point{x: p.x + 1, y: p.y}
}
func moveLeft(p point) point {
	return point{x: p.x - 1, y: p.y}
}
func moveUp(p point) point {
	return point{x: p.x, y: p.y + 1}
}
func moveDown(p point) point {
	return point{x: p.x, y: p.y - 1}
}

func part1(filename string) int {
	directions := make(map[string]func(point) point)
	directions["L"] = moveLeft
	directions["R"] = moveRight
	directions["D"] = moveDown
	directions["U"] = moveUp

	visited := make([]point, 0)
	head := point{x: 0, y: 0}
	tail := point{x: 0, y: 0}
	moves := getMoves(filename)
	var diff [2]int
	for _, mv := range moves {
		for i := 0; i < mv.magnitude; i++ {
			head = directions[mv.direction](head)
		}
		diff[0] = head.x - tail.x
		diff[1] = head.y - tail.y
		switch diff {
		// two away, in a straight line
		case [2]int{-2, 0}:
			tail = moveLeft(tail)
		case [2]int{2, 0}:
			tail = moveRight(tail)
		case [2]int{0, 2}:
			tail = moveUp(tail)
		case [2]int{0, -2}:
			tail = moveDown(tail)
		// 1 away, or on the same point: do nothing
		case (math.Abs(diff[0])+math.Abs(diff[1]) <= 1):
			// do nothing
		// diagonal
		case [2]int{-1, 2}:
			tail = moveUp(moveLeft(tail))
		case [2]int{1, 2}:
			tail = moveUp(moveRight(tail))
		case [2]int{-2, 1}:
			tail = moveLeft(moveUp(tail))
		case [2]int{2, 1}:
			tail = moveRight(moveUp(tail))
		case [2]int{-2, -1}:
			tail = moveDown(moveLeft(tail))
		case [2]int{2, -1}:
			tail = moveDown(moveRight(tail))
		case [2]int{-1, -2}:
			tail = moveLeft(moveDown(tail))
		case [2]int{1, -2}:
			tail = moveDown(moveRight(tail))
		default:
			panic("This case is not covered")
		}
		addIfNotPresent(visited[:], tail)
	}
	return len(visited)
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
	answer = part1("sample.txt")
	fmt.Println(answer)
	fmt.Println("the answer to part 1 is ")
	fmt.Println(part1("input.txt"))

	if part2("sample.txt") != 8 {
		panic("wrong answer to sample input for part2")
	}
	fmt.Println("the answer to part 2 is ")
	fmt.Println(part2("input.txt"))

	// how exactly do for loops work?
	var k int
	for k = 0; k < 10; k++ {
	}
	// after the loop, k==10
}
