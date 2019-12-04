package main

import (
	"fmt"
	"strconv"
)

func main() {
	s := "1113122113"
	for i := 0; i < 50; i++ {
		if i%10 == 0 {
			fmt.Print(i)
		} else {
			fmt.Print(".")
		}
		ns := ""
		cc := rune(s[0])
		ci := 0
		for _, c := range s {
			if cc == c {
				ci++
			} else {
				ns += strconv.Itoa(ci) + string(cc)
				ci = 1
				cc = c
			}
		}
		ns += strconv.Itoa(ci) + string(cc)
		s = ns
	}
	fmt.Println("length:", len(s))
}
