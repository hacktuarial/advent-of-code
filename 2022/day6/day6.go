package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func allDifferent(str string) bool {
	if len(str) == 0 {
		return true
	}
	for i := 1; i < len(str); i++ {
		if str[0] == str[i] {
			return false
		}
	}
	return allDifferent(str[1:])
}

func findMarker(str string, k int) int {
	for i := 0; i+k < len(str); i++ {
		if allDifferent(str[i : i+k]) {
			return i + k
		}
	}
	return -1
}

func day6(filename string, k int) int {
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		txt := scanner.Text()
		return findMarker(txt, k)
	}
	panic("panic")
}

func main() {
	// part 1
	fmt.Println("the answer to part1 is ")
	fmt.Println(day6("input.txt", 4))
	// part 2
	fmt.Println("the answer to part2 is ")
	fmt.Println(day6("input.txt", 14))
	// if answer != "MCD" {
	// 	panic("wrong answer to sample problem, part2")
	// }
	// fmt.Println("the answer to part2 is " + day5("input.txt", false, false))
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
