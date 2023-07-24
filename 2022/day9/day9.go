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

func day9(filename string, nKnots int) int {
	directions := make(map[string]func(point) point)
	directions["L"] = moveLeft
	directions["R"] = moveRight
	directions["D"] = moveDown
	directions["U"] = moveUp

	visited := make([]point, 1)
	visited = addIfNotPresent(visited, point{x: 0, y: 0})
	knots := make([]point, 10, 10)
	for i := 0; i < nKnots; i++ {
		knots[i] = point{x: 0, y: 0}
	}
	moves := getMoves(filename)
	var diff [2]int
	for _, mv := range moves {
		fmt.Println(formatMove(mv))
		for i := 0; i < mv.magnitude; i++ {
			// move the head
			knots[0] = directions[mv.direction](knots[0])
			// now, move the tails one by one
			for k := 1; k < nKnots; k++ {
				// fmt.Println("head is at " + formatPoint(head) + ", tail is at" + formatPoint(tail))
				// head is at k-1, tail is at k
				diff[0] = knots[k-1].x - knots[k].x
				diff[1] = knots[k-1].y - knots[k].y
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
							knots[k] = moveRight(knots[k])
						} else if diff[0] == -2 {
							knots[k] = moveLeft(knots[k])
						} else if diff[1] == 2 {
							knots[k] = moveUp(knots[k])
						} else if diff[1] == -2 {
							knots[k] = moveDown(knots[k])
						} else {
							panic("not possible (1)")
						}
					}
				default:
					// distance of 3+
					// has to be a diagonal move
					if diff[0] > 0 {
						knots[k] = moveRight(knots[k])
					} else {
						knots[k] = moveLeft(knots[k])
					}
					if diff[1] > 0 {
						knots[k] = moveUp(knots[k])
					} else {
						knots[k] = moveDown(knots[k])
					}
					// default:
					// 	for j := 0; j < nKnots; j++ {
					// 		fmt.Println(formatPoint(knots[j]))
					// 	}
					// 	panic("not possible (2)")
				}
				if k == nKnots-1 {
					fmt.Println("adding this point " + formatPoint(knots[k]))
					// only track the last tail
					visited = addIfNotPresent(visited, knots[k])
				}
				// fmt.Println("after moving, tail is at " + formatPoint(tail))
			}
		}
	}
	fmt.Println("here are all of the points visited by the tail")
	for _, visit := range visited {
		fmt.Println(formatPoint(visit))
	}
	return len(visited)
}

func main() {
	var answer int
	// answer = day9("sample.txt", 2)
	// fmt.Println(answer)
	// fmt.Println("the answer to part 1 is ")
	// answer = day9("input.txt", 2)
	// if answer != 5858 {
	// 	panic("wrong answer to part1")
	// }

	answer = day9("sample.txt", 10)
	if answer != 1 {
		panic("wrong answer to sample problem, part2")
	}
	fmt.Println("the answer to part 2 is")
	fmt.Println(day9("input.txt", 10))

}
