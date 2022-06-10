package main

import (
	"fmt"
	"log"
	"time"
	ugg "user_gauss_params/userGenerateGauss"
)

func main() {
	start := time.Now()
	raw_data_path := "/root/KL_Divergence/user_gauss_params/data/user_1.csv"
	individual_Gauss := ugg.GenerateGauss(raw_data_path)
	fmt.Println("individual_Gauss", individual_Gauss)
	elapsed := time.Since(start)
	log.Printf("user_1_mnist_train Gauss generation took %s", elapsed)

	// singapore_Gauss := ugg.GenerateGauss(raw_data_path)
	// fmt.Println("singapore Gauss", singapore_Gauss)
}
