package main

import (
	"fmt"
	"path/filepath"
	"runtime"
	sge "server_entropy_percent/serverGenerateEntropy"
)

var (
	_, b, _, _ = runtime.Caller(0)
	basepath   = filepath.Dir(b)
)

func main() {
	dir_path := basepath + "/data/users_individual_gauss"
	entropy_percent_user := sge.GenerateEntropy(dir_path)
	fmt.Println("entropy_percent_user", entropy_percent_user)
}
