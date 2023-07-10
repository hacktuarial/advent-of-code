package main

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestFindMarker(t *testing.T) {
	assert := assert.New(t)
	assert.Equal(findMarker("bvwbjplbgvbhsrlpgdmjqwftvncz"), 5)
	assert.Equal(findMarker("nppdvjthqldpwncqszvftbrmjlhg"), 6)
	assert.Equal(findMarker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"), 10)
	assert.Equal(findMarker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"), 11)
}
