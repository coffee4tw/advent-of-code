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

	dist := map[string]map[string]int{}
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
		fields := strings.Fields(line)

		c1 := fields[0]
		c2 := fields[2]
		d, _ := strconv.Atoi(fields[4])

		if m, ok := dist[c1]; !ok {
			dist[c1] = map[string]int{c2: d}
		} else {
			m[c2] = d
		}
		if m, ok := dist[c2]; !ok {
			dist[c2] = map[string]int{c1: d}
		} else {
			m[c1] = d
		}
	}

	n := len(dist)
	i := 0
	idx := []int{}
	keys := []string{}
	for k := range dist {
		keys = append(keys, k)
		idx = append(idx, i)
		i++
	}
	perms := permutations(idx, n)

	min := int(2e16)
	max := 0
	for _, perm := range perms {
		sum := 0
		for i := 0; i < len(perm)-1; i++ {
			sum += dist[keys[perm[i]]][keys[perm[i+1]]]
		}
		if sum < min {
			min = sum
		} else if sum > max {
			max = sum
		}
	}

	fmt.Printf("shortest=%v longest=%v\n", min, max)
}

func permutations(iterable []int, r int) [][]int {
	pool := iterable
	n := len(pool)

	if r > n {
		return nil
	}

	res := [][]int{}

	indices := make([]int, n)
	for i := range indices {
		indices[i] = i
	}

	cycles := make([]int, r)
	for i := range cycles {
		cycles[i] = n - i
	}

	result := make([]int, r)
	for i, el := range indices[:r] {
		result[i] = pool[el]
	}

	res = append(res, append([]int(nil), result...))

	for n > 0 {
		i := r - 1
		for ; i >= 0; i -= 1 {
			cycles[i] -= 1
			if cycles[i] == 0 {
				index := indices[i]
				for j := i; j < n-1; j += 1 {
					indices[j] = indices[j+1]
				}
				indices[n-1] = index
				cycles[i] = n - i
			} else {
				j := cycles[i]
				indices[i], indices[n-j] = indices[n-j], indices[i]

				for k := i; k < r; k += 1 {
					result[k] = pool[indices[k]]
				}

				res = append(res, append([]int(nil), result...))

				break
			}
		}

		if i < 0 {
			return res
		}

	}

	return res
}
