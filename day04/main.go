package main

import (
	"crypto/md5"
	"encoding/hex"
	"fmt"
	"io"
	"strconv"
	"strings"
)

func main() {
	secret := "iwrupvqb"
	num := 1

	for {
		key := secret + strconv.Itoa(num)
		h := md5.New()
		io.WriteString(h, key)
		res := hex.EncodeToString(h.Sum(nil))
		// fmt.Println(key, res)
		if strings.HasPrefix(res, "000000") {
			fmt.Println("Result (000000):", num)
			break
		} else if strings.HasPrefix(res, "00000") {
			fmt.Println("Result (00000):", num)
		}
		num++
	}
}
