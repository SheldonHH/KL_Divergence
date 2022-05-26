package main

import (
	"fmt"
	ugg "user_gauss_params/userGenerateGauss"
)

func main() {
	raw_data_path := "user_gauss_params/data/user1_data.csv"
	individual_Gauss := ugg.GenerateGauss(raw_data_path)
	fmt.Println("individual_Gauss", individual_Gauss)
}