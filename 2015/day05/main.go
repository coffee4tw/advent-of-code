package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strings"
)

func main() {
	part1()
	part2()
}

func part2() {
	file, err := os.Open("input.txt")
	if err != nil {
		panic(err)
	}
	reader := bufio.NewReader(file)

	var lb []byte
	var line string
	nice, naughty := 0, 0
	for {
		// read each character one by one
		if lb, _, err = reader.ReadLine(); err != nil {
			if err == io.EOF {
				break
			} else {
				panic(err)
			}
		}
		line = string(lb)

		// It contains a pair of any two letters that appears at least twice in the string without overlapping, like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
		found := false
		for i := 0; i < len(line)-1; i++ {
			if strings.Count(line, line[i:i+2]) > 1 {
				found = true
				break
			}
		}
		if !found {
			naughty++
			continue
		}

		// It contains at least one letter which repeats with exactly one letter between them, like xyx, abcdefeghi (efe), or even aaa.
		found = false
		for i := 0; i < len(line)-2; i++ {
			if line[i] == line[i+2] {
				found = true
				break
			}
		}
		if !found {
			naughty++
			continue
		}

		nice++
	}

	fmt.Println("nice:", nice, "naughty:", naughty)
}

func part1() {
	file, err := os.Open("input.txt")
	if err != nil {
		panic(err)
	}
	reader := bufio.NewReader(file)

	var lb []byte
	var line string
	nice, naughty := 0, 0
	for {
		// read each character one by one
		if lb, _, err = reader.ReadLine(); err != nil {
			if err == io.EOF {
				break
			} else {
				panic(err)
			}
		}
		line = string(lb)

		// It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
		c := 0
		for _, r := range "aeiou" {
			c += strings.Count(line, string(r))
		}
		if c < 3 {
			naughty++
			continue
		}

		// It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
		found := false
		for i := 0; i < len(line)-1; i++ {
			if line[i] == line[i+1] {
				found = true
				break
			}
		}
		if !found {
			naughty++
			continue
		}

		// It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.
		found = false
		for _, s := range []string{"ab", "cd", "pq", "xy"} {
			if strings.Contains(line, s) {
				found = true
				break
			}
		}
		if found {
			naughty++
			continue
		}

		nice++
	}

	fmt.Println("nice:", nice, "naughty:", naughty)
}
