package main

import (
	"fmt"
	"strings"
)

func main() {
	var s string
	for s = "vzbxkghb"; !valid(s); s = inc(s) {
	}
	fmt.Println(s)
	for s = inc(s); !valid(s); s = inc(s) {
	}
	fmt.Println(s)
}

// Passwords may not contain the letters i, o, or l, as these letters can be mistaken for other characters and are therefore confusing.
func inc(s string) string {
	for i := len(s) - 1; i >= 0; i-- {
		switch rune(s[i]) {
		case 'z':
			s = replace(s, 'a', i)
		case 'i', 'o', 'l':
			return inc(replace(s, rune(s[i])+1, i))
		default:
			return replace(s, rune(s[i])+1, i)
		}
	}
	return s
}

func replace(s string, r rune, i int) string {
	if i == len(s)-1 {
		return s[:i] + string(r)
	} else {
		return s[:i] + string(r) + s[i+1:]
	}
}

// Passwords must include one increasing straight of at least three letters, like abc, bcd, cde, and so on, up to xyz. They cannot skip letters; abd doesn't count.
// Passwords must contain at least two different, non-overlapping pairs of letters, like aa, bb, or zz.
func valid(s string) bool {
	found := false
	for i := 0; i < len(s)-2; i++ {
		if rune(s[i])+1 == rune(s[i+1]) && rune(s[i+1])+1 == rune(s[i+2]) {
			found = true
			break
		}
	}
	if !found {
		return false
	}

	if strings.Contains(s, "i") || strings.Contains(s, "o") || strings.Contains(s, "l") {
		return false
	}

	n := 0
	for i := 0; i < len(s)-1; i++ {
		if strings.Contains(s, string(s[i])+string(s[i])) {
			n++
		}
	}
	if n/2 < 2 {
		return false
	}

	return true
}
