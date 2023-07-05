package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func initializeSample() []Stack {
	stacks := make([]Stack, 3+1)
	stacks[1].Push("Z")
	stacks[1].Push("N")
	stacks[2].Push("M")
	stacks[2].Push("C")
	stacks[2].Push("D")
	stacks[3].Push("P")
	return stacks
}

//	[M]     [B]             [N]
//
// [T]     [H]     [V] [Q]         [H]
// [Q]     [N]     [H] [W] [T]     [Q]
// [V]     [P] [F] [Q] [P] [C]     [R]
// [C]     [D] [T] [N] [N] [L] [S] [J]
// [D] [V] [W] [R] [M] [G] [R] [N] [D]
// [S] [F] [Q] [Q] [F] [F] [F] [Z] [S]
// [N] [M] [F] [D] [R] [C] [W] [T] [M]
//
//	1   2   3   4   5   6   7   8   9
func initializeFull() []Stack {
	stacks := make([]Stack, 9+1)
	stackInputs := make([]string, len(stacks))
	stackInputs[1] = "NSDCVQT"
	stackInputs[2] = "MFV"
	stackInputs[3] = "FQWDPNHM"
	stackInputs[4] = "DQRTF"
	stackInputs[5] = "RFMNQHVB"
	stackInputs[6] = "CFGNPWQ"
	stackInputs[7] = "WFRLCT"
	stackInputs[8] = "TZNS"
	stackInputs[9] = "MSDJRQHN"
	for i, s := range stackInputs {
		for j, _ := range s {
			stacks[i].Push(s[j : j+1])
		}
	}
	return stacks
}

func move(from int, to int, stacks []Stack) {
	stacks[to].Push(stacks[from].Pop())
	for i, stack := range stacks {
		msg := "stack " + strconv.FormatInt(int64(i), 10) + " has " + strconv.FormatInt(int64(stack.Len()), 10) + " elements"
		// fmt.Println(msg)
	}
}

func part1(filename string, isSample bool) string {
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	var stacks []Stack
	if isSample {
		stacks = initializeSample()
	} else {
		stacks = initializeFull()
	}
	answer := ""
	for scanner.Scan() {
		txt := scanner.Text()
		if !strings.Contains(txt, "move") {
			continue
		}
		howMany, _ := strconv.Atoi(strings.Split(txt, " ")[1])
		from, _ := strconv.Atoi(strings.Split(txt, " ")[3])
		to, _ := strconv.Atoi(strings.Split(txt, " ")[5])
		for i := 0; i < howMany; i++ {
			// use a slice!
			move(from, to, stacks[:])
		}
	}

	for _, stack := range stacks[1:] {
		val := stack.Pop().(string)
		answer += val
	}
	return answer
}

func main() {
	// part 1
	answer := part1("sample.txt", true)
	if answer != "CMZ" {
		panic("wrong answer to sample problem, part1")
	}
	fmt.Println(part1("input.txt", false))
	// part 2
	// answer = part2("sample.txt")
	// if answer != 4 {
	// 	panic("wrong answer to sample problem, part2")
	// }
	// fmt.Println(part2("input.txt"))
}

// https://github.com/golang-collections/collections/blob/master/stack/stack.go
type (
	Stack struct {
		top    *node
		length int
	}
	node struct {
		value interface{}
		prev  *node
	}
)

// Create a new stack
func New() *Stack {
	return &Stack{nil, 0}
}

// Return the number of items in the stack
func (this *Stack) Len() int {
	return this.length
}

// View the top item on the stack
func (this *Stack) Peek() interface{} {
	if this.length == 0 {
		return nil
	}
	return this.top.value
}

// Pop the top item of the stack and return it
func (this *Stack) Pop() interface{} {
	if this.length == 0 {
		return nil
	}

	n := this.top
	this.top = n.prev
	this.length--
	return n.value
}

// Push a value onto the top of the stack
func (this *Stack) Push(value interface{}) {
	n := &node{value, this.top}
	this.top = n
	this.length++
}
