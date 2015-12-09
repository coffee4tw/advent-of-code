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

	code := 0
	escaped := 0
	unescaped := 0
	for {
		// read each line one by one
		var lb []byte
		if lb, _, err = reader.ReadLine(); err != nil {
			if err == io.EOF {
				break
			} else {
				panic(err)
			}
		}
		line := string(lb)
		code += len(line)

		l1, _ := strconv.Unquote(line)
		unescaped += len(l1)

		l2 := strconv.Quote(line)
		escaped += len(l2)
	}

	fmt.Printf("code=%v unescaped=%v(-%v) escaped=%v(+%v)\n", code, unescaped, (code - unescaped), escaped, (escaped - code))
}
