package main

import (
	sge "server_entropy_percent/serverGenerateEntropy"
	"fmt"
)

func main() {
	dir_path := "server_entropy_percent/data/server_gauss_joint"
	entropy_percent_user := sge.GenerateEntropy(dir_path)
	fmt.Println("entropy_percent_user", entropy_percent_user)
}
