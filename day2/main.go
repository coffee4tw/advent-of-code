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
	paper := 0
	ribbon := 0
	for {
		// read each character one by one
		if lb, _, err = reader.ReadLine(); err != nil {
			if err == io.EOF {
				break
			} else {
				panic(err)
			}
		}

		// get the dimensions from each line
		line := string(lb)
		dim := strings.Split(line, "x")
		if len(dim) != 3 {
			panic("incorrect input format")
		}

		dims := make([]int, len(dim))
		for i := range dim {
			dims[i], err = strconv.Atoi(dim[i])
			if err != nil {
				panic(err)
			}
		}

		// calculate the box surface plus slack
		surface := 2*dims[0]*dims[1] + 2*dims[0]*dims[2] + 2*dims[1]*dims[2]
		volume := dims[0] * dims[1] * dims[2]
		slack := dims[0] * dims[1]
		if slack > dims[0]*dims[2] {
			slack = dims[0] * dims[2]
		}
		if slack > dims[1]*dims[2] {
			slack = dims[1] * dims[2]
		}
		perimeter := dims[0] + dims[1]
		if perimeter > dims[0]+dims[2] {
			perimeter = dims[0] + dims[2]
		}
		if perimeter > dims[1]+dims[2] {
			perimeter = dims[1] + dims[2]
		}

		paper += surface + slack
		ribbon += 2*perimeter + volume
	}

	fmt.Println("Feet of paper:", paper)
	fmt.Println("Feet of ribbon:", ribbon)
}
