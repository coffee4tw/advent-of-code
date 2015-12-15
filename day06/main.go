package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

func main() {
	file, err := os.Open("input.txt")
	if err != nil {
		panic(err)
	}
	reader := bufio.NewReader(file)

	var lb []byte
	var line string
	grid := make([][]bool, 1000)
	for i := range grid {
		grid[i] = make([]bool, 1000)
	}

	grid2 := make([][]int, 1000)
	for i := range grid2 {
		grid2[i] = make([]int, 1000)
	}
	var x1, x2, y1, y2 int
	var op int
	for {
		// read each line one by one
		if lb, _, err = reader.ReadLine(); err != nil {
			if err == io.EOF {
				break
			} else {
				panic(err)
			}
		}
		line = string(lb)
		fields := strings.Fields(line)

		switch fields[0] {
		case "turn":
			coo := strings.Split(fields[2], ",")
			x1, _ = strconv.Atoi(coo[0])
			y1, _ = strconv.Atoi(coo[1])
			coo = strings.Split(fields[4], ",")
			x2, _ = strconv.Atoi(coo[0])
			y2, _ = strconv.Atoi(coo[1])
			switch fields[1] {
			case "on":
				op = 1
			case "off":
				op = 0
			}
		case "toggle":
			coo := strings.Split(fields[1], ",")
			x1, _ = strconv.Atoi(coo[0])
			y1, _ = strconv.Atoi(coo[1])
			coo = strings.Split(fields[3], ",")
			x2, _ = strconv.Atoi(coo[0])
			y2, _ = strconv.Atoi(coo[1])
			op = 2
		}

		for i := x1; i <= x2; i++ {
			for j := y1; j <= y2; j++ {
				switch op {
				case 0:
					grid[i][j] = false
					if grid2[i][j] > 0 {
						grid2[i][j]--
					}
				case 1:
					grid[i][j] = true
					grid2[i][j]++
				case 2:
					grid[i][j] = !grid[i][j]
					grid2[i][j] += 2
				}
			}
		}
	}

	count := 0
	bright := 0
	for i := range grid {
		for j := range grid[i] {
			if grid[i][j] {
				count++
			}
			bright += grid2[i][j]
		}
	}

	fmt.Println("count:", count)
	fmt.Println("bright:", bright)
}
