package main

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestFindMarker(t *testing.T) {
	assert := assert.New(t)
	assert.Equal(findMarker("bvwbjplbgvbhsrlpgdmjqwftvncz", 4), 5)
	assert.Equal(findMarker("nppdvjthqldpwncqszvftbrmjlhg", 4), 6)
	assert.Equal(findMarker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4), 10)
	assert.Equal(findMarker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4), 11)
	//part2
	assert.Equal(findMarker("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14), 19)
}
