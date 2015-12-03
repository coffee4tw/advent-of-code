package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
)

func main() {
	file, err := os.Open("input.txt")
	if err != nil {
		panic(err)
	}

	reader := bufio.NewReader(file)

	var c rune
	n := 2
	i := 0
	x := make([]int, n)
	y := make([]int, n)
	visited := map[string]bool{"0,0": true}
	houses := 1
	for {
		// read each character one by one
		if c, _, err = reader.ReadRune(); err != nil {
			if err == io.EOF {
				break
			} else {
				panic(err)
			}
		}

		// only count characters that we care about to go up, down, right and left
		switch c {
		case '^':
			y[i]++
		case 'v':
			y[i]--
		case '>':
			x[i]++
		case '<':
			x[i]--
		}

		// check if we visited here already
		loc := strconv.Itoa(x[i]) + "," + strconv.Itoa(y[i])
		if _, ok := visited[loc]; !ok {
			houses++
			visited[loc] = true
		}

		i = (i + 1) % n
	}

	fmt.Println("Houses:", houses)
}
