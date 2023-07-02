package day2

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestRockPaperScissors(t *testing.T) {
	assert := assert.New(t)
	assert.Equal(0, play(1, 1))
	assert.Equal(0, play(2, 2))
	assert.Equal(0, play(3, 3))
	// paper(2) beats rock(1)
	assert.Equal(1, play(1, 2))
	assert.Equal(-1, play(2, 1))
	// scissors(3) beats rock(2)
	assert.Equal(1, play(2, 3))
	assert.Equal(-1, play(3, 2))
	// rock(1) beats scissors(3)

}