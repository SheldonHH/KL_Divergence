package main

import (
	"fmt"
	ugg "user_gauss_params/userGenerateGauss"
	"log"
	"time"
)

func main() {
	start := time.Now()
	raw_data_path := "user_gauss_params/data/user_1_mnist_train.csv"
	individual_Gauss := ugg.MixGauss(raw_data_path)
	fmt.Println("individual_Gauss", individual_Gauss)
	elapsed := time.Since(start)
	log.Printf("user_1_mnist_train Gauss generation took %s", elapsed)

	// singapore_Gauss := ugg.GenerateGauss(raw_data_path)
	// fmt.Println("singapore Gauss", singapore_Gauss)
}
