package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"reflect"
)

func main() {
	data, err := ioutil.ReadFile("input.txt")
	if err != nil {
		panic(err)
	}
	fmt.Println("total:", sum(data))

	o := map[string]interface{}{}
	if err := json.Unmarshal(data, &o); err != nil {
		panic(err)
	}
	fmt.Println("excluded:", sumExclude(o, "red"))
}

func sum(data []byte) int {
	total := 0
	dec := json.NewDecoder(bytes.NewReader(data))
	for {
		t, err := dec.Token()
		if err == io.EOF {
			break
		}
		if err != nil {
			panic(err)
		}
		if reflect.TypeOf(t).Name() == "float64" {
			total += int(t.(float64))
		}
	}
	return total
}

func sumExclude(data interface{}, excl string) int {
	switch data.(type) {
	case float64:
		return int(data.(float64))
	case []interface{}:
		ar := data.([]interface{})
		total := 0
		for i := range ar {
			total += sumExclude(ar[i], excl)
		}
		return total
	case map[string]interface{}:
		m := data.(map[string]interface{})
		incl := true
		total := 0
		for _, v := range m {
			if reflect.TypeOf(v).Name() == "string" && v.(string) == "red" {
				incl = false
				break
			}
			total += sumExclude(v, excl)
		}
		if incl {
			return total
		} else {
			return 0
		}
	}
	return 0
}
