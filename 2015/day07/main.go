package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
	"unicode"
)

type Wire struct {
	Name    string
	Parents []*Wire
	Value   []string
}

var (
	visited = map[string]bool{}
)

func (w *Wire) Order() []*Wire {
	nodes := []*Wire{}
	for i := range w.Parents {
		p := w.Parents[i]
		if _, ok := visited[p.Name]; !ok {
			nodes = append(nodes, p.Order()...)
		}
	}
	nodes = append(nodes, w)
	visited[w.Name] = true
	return nodes
}

func (w *Wire) String() string {
	return w.Name
}

func main() {
	file, err := os.Open("input.txt")
	if err != nil {
		panic(err)
	}
	reader := bufio.NewReader(file)

	wires := map[string]uint16{}
	overrides := map[string]uint16{
		"b": uint16(16076),
	}
	wtree := map[string]*Wire{}
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

		// build tree
		var wire *Wire
		wn := fields[len(fields)-1]
		if w, ok := wtree[wn]; !ok {
			wire = &Wire{
				Name:    wn,
				Parents: []*Wire{},
			}
			wtree[wn] = wire
		} else {
			wire = w
		}
		wire.Value = fields[0 : len(fields)-2]
		for i := 0; i < len(fields)-2; i++ {
			if unicode.IsLower(rune(fields[i][0])) {
				wn := fields[i]
				if _, ok := wtree[wn]; !ok {
					wtree[fields[i]] = &Wire{
						Name:    wn,
						Parents: []*Wire{},
					}
				}
				wire.Parents = append(wire.Parents, wtree[wn])
			}
		}
	}

	// fmt.Println(wtree["a"].Order())

	for _, w := range wtree["a"].Order() {
		// read what's going on
		fields := w.Value
		dest := w.Name
		org := fields[0]
		switch len(fields) {
		case 1:
			// ASSIGNMENT
			if _, ok := overrides[dest]; ok {
				wires[dest] = overrides[dest]
			} else {
				if i, err := strconv.Atoi(org); err != nil {
					wires[dest] = wires[org]
				} else {
					wires[dest] = uint16(i)
				}
			}
		case 2:
			// NOT
			org = fields[1]
			if i, err := strconv.Atoi(org); err != nil {
				wires[dest] = ^wires[org]
			} else {
				wires[dest] = ^uint16(i)
			}
		case 3:
			org2 := fields[2]
			switch fields[1] {
			case "AND":
				if i, err := strconv.Atoi(org); err != nil {
					wires[dest] = wires[org] & wires[org2]
				} else {
					wires[dest] = uint16(i) & wires[org2]
				}
			case "OR":
				wires[dest] = wires[org] | wires[org2]
			case "RSHIFT":
				if i, err := strconv.Atoi(org2); err != nil {
					wires[dest] = wires[org] >> wires[org2]
				} else {
					wires[dest] = wires[org] >> uint16(i)
				}
			case "LSHIFT":
				if i, err := strconv.Atoi(org2); err != nil {
					wires[dest] = wires[org] << wires[org2]
				} else {
					wires[dest] = wires[org] << uint16(i)
				}
			}
		default:
			fmt.Println(w.Name)
			fmt.Println(w.Value)
			fmt.Println(w.Parents)
			panic("missed one")
		}
	}

	fmt.Println("wire a:", wires["a"])
}
