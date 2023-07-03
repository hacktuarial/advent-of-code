package main

import (
	"github.com/stretchr/testify/assert"
	"strings"
	"testing"
)

func TestFindOverlap(t *testing.T) {
	assert := assert.New(t)
	assert.Equal("a" < "b", true)
	s1 := strings.Split("a", "")
	s2 := strings.Split("a", "")
	assert.Equal("a", findOverlap(s1, s2))
	s1 = strings.Split("abc", "")
	s2 = strings.Split("bd", "")
	assert.Equal("b", findOverlap(s1, s2))
	s1 = strings.Split("abcde", "")
	s2 = strings.Split("ef", "")
	assert.Equal("e", findOverlap(s1, s2))
}
