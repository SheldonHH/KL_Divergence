package main

import (
	"encoding/csv"
	"fmt"
	"io/ioutil"
	"log"
	"strings"
)

func main() {
	entropy_percent_user := ugg.GenerateEntropy("user1 user2")
	fmt.Println("entropy_percent_user", entropy_percent_user)
}
