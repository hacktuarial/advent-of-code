package main

import (
    "bufio"
    "fmt"
    "log"
    "os"
	"strconv"
)

func read_file(filename string) int {
    file, err := os.Open(filename)
    if err != nil {
        log.Fatal(err)
    }
    defer file.Close()

    scanner := bufio.NewScanner(file)
    // optionally, resize scanner's capacity for lines over 64K, see next example
	max := 0
	runningTotal := 0
    for scanner.Scan() {
		// fmt.Println(runningTotal)
        txt := scanner.Text()
		if (txt == "") {
			if (runningTotal > max) {
				max = runningTotal
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
	return max
}

func main() {
	answer := read_file("sample.txt")
	if (answer != 24000) {
		panic("wrong answer to sample problem")
	}
	fmt.Println(read_file("input.txt"))
}