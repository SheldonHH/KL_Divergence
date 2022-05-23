package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
)

type dict map[string]map[string]interface{}

func main() {
	gauss_dict := obtainMap("../data_sample/joint/consolidated_gauss_params.json")
	fmt.Println(gauss_dict)
	percent_dict := obtainMap("../data_sample/joint/consolidated_percent.json")
	fmt.Println(percent_dict)
}

func obtainMap(jsonStrPath string) (sg dict) {
	jsonFile, err := os.Open(jsonStrPath)
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println("Successfully Opened users.json")
	// defer the closing of our percent_jsonFile so that we can parse it later on
	defer jsonFile.Close()
	byteValue, _ := ioutil.ReadAll(jsonFile)
	var result map[string]map[string]interface{}
	json.Unmarshal([]byte(byteValue), &result)
	sg = result
	return
}
