package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"runtime"
	"time"
	ugg "user_gauss_params/userGenerateGauss"
)

var (
	_, b, _, _ = runtime.Caller(0)
	basepath   = filepath.Dir(b)
	username   = "user_1"
)

func main() {
	start := time.Now()
	fmt.Println(basepath)
	raw_data_path := basepath + "/data/" + username + ".csv"
	individual_Gauss := ugg.GenerateGauss(raw_data_path)
	fmt.Println("individual_Gauss", individual_Gauss)
	plan, _ := ioutil.ReadFile(basepath + "/data/features/freq/dynamic_features_gauss.json")
	var data interface{}
	err := json.Unmarshal(plan, &data)
	if err != nil {
		fmt.Print("err:", err)
	}
	fmt.Println("data", data)
	e := os.Remove(basepath + "/data/features/freq/dynamic_features_gauss.json")
	if e != nil {
		log.Fatal(e)
	}
	elapsed := time.Since(start)
	log.Printf(username+"'s Gauss generation took %s", elapsed)
	// singapore_Gauss := ugg.GenerateGauss(raw_data_path)
	// fmt.Println("singapore Gauss", singapore_Gauss)
}
