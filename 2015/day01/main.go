package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
)

func main() {
	file, err := os.Open("input.txt")
	if err != nil {
		panic(err)
	}

	reader := bufio.NewReader(file)

	var c rune
	result := 0
	enter := 0
	found := false
	for {
		// read each character one by one
		if c, _, err = reader.ReadRune(); err != nil {
			if err == io.EOF {
				break
			} else {
				panic(err)
			}
		}

		// only count characters that we care about to go up and down
		switch c {
		case '(':
			result++
		case ')':
			result--
		}

		// if we haven't found the basement yet, continue to advance the index until we enter it
		if !found {
			enter++

			if result == -1 {
				found = true
			}
		}
	}

	fmt.Println("Floor:", result)
	fmt.Println("Enter basement:", enter)
}
