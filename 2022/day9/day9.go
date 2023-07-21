package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

type move struct {
	direction string
	magnitude int
}

func absValue(x int) int {
	if x < 0 {
		return -x
	}
	return x
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
		txt := strings.Split(scanner.Text(), " ")
		mag, _ := strconv.Atoi(txt[1])
		if mag == 0 {
			panic(scanner.Text())
		}
		moves = append(moves, move{direction: txt[0], magnitude: mag})
	}
	return moves
}

func addIfNotPresent(visited []point, new point) []point {
	for _, p := range visited {
		if p.x == new.x && p.y == new.y {
			return visited
		}
	}
	visited = append(visited, new)
	// fmt.Println("tail has visited this many points:")
	// fmt.Println(len(visited))
	return visited
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

func formatPoint(p point) string {
	out := "("
	out += strconv.FormatInt(int64(p.x), 10)
	out += ","
	out += strconv.FormatInt(int64(p.y), 10)
	out += ")"
	return out
}
func formatMove(m move) string {
	out := m.direction + " "
	out += strconv.FormatInt(int64(m.magnitude), 10)
	return out
}

func part1(filename string) int {
	directions := make(map[string]func(point) point)
	directions["L"] = moveLeft
	directions["R"] = moveRight
	directions["D"] = moveDown
	directions["U"] = moveUp

	visited := make([]point, 1)
	visited = addIfNotPresent(visited, point{x: 0, y: 0})
	head := point{x: 0, y: 0}
	tail := point{x: 0, y: 0}
	moves := getMoves(filename)
	var diff [2]int
	for _, mv := range moves {
		fmt.Println(formatMove(mv))
		for i := 0; i < mv.magnitude; i++ {
			head = directions[mv.direction](head)
			fmt.Println("head is at " + formatPoint(head) + ", tail is at" + formatPoint(tail))
			diff[0] = head.x - tail.x
			diff[1] = head.y - tail.y
			totalDiff := absValue(diff[0]) + absValue(diff[1])
			switch totalDiff {
			case 0:
				// tail and head are in the same place
				continue
			case 1:
				// tail is close enough to head. don't move it
				continue
			case 2:
				// (+/- 1, +/- 1) or (+/- 2, 0) or (0, +/- 2)
				if absValue(diff[1]) == 1 {
					// tail is close enough to head. don't move it
					continue
				} else {
					if diff[0] == 2 {
						tail = moveRight(tail)
					} else if diff[0] == -2 {
						tail = moveLeft(tail)
					} else if diff[1] == 2 {
						tail = moveUp(tail)
					} else if diff[1] == -2 {
						tail = moveDown(tail)
					} else {
						panic("not possible")
					}
				}
			case 3:
				// has to be a diagonal move
				if diff[0] > 0 {
					tail = moveRight(tail)
				} else {
					tail = moveLeft(tail)
				}
				if diff[1] > 0 {
					tail = moveUp(tail)
				} else {
					tail = moveDown(tail)
				}
			default:
				panic("not possible")
			}
			visited = addIfNotPresent(visited, tail)
			fmt.Println("after moving, tail is at " + formatPoint(tail))
		}
	}
	for _, visit := range visited {
		fmt.Println(formatPoint(visit))
	}
	return len(visited)
}

func main() {
	answer := part1("sample.txt")
	fmt.Println(answer)
	fmt.Println("the answer to part 1 is ")
	fmt.Println(part1("input.txt"))

}
