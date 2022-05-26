package main

import (
	"encoding/csv"
	"fmt"
	"io/ioutil"
	"log"
	"strings"
)

// go get github.com/gopherdata/gophernotes
func main() {

	raw_data_path := "/root/KL_Divergence/data/user_1_data.csv"
	individual_Gauss := singapore.GenerateGauss(raw_data_path)
	entropy_percent_user := singapore.GenerateEntropy("user1 user2")
	fmt.Println("individual_Gauss", individual_Gauss)
	fmt.Println("entropy_percent_user", entropy_percent_user)
	// newUpdate := modelTraining(privateData)
	// fmt.Println(newUpdate.senderID)
}

func readPrivateData(filePath string) map[int][]string { //用户读取私人数据
	dat, err := ioutil.ReadFile(filePath)
	if err != nil {
		log.Fatal(err)
	}
	r := csv.NewReader(strings.NewReader(string(dat[:])))

	record, err := r.ReadAll() //record为与CSV同样结构的二维数组
	if err != nil {
		panic("Fail to read csv file!")
	}
	mapCsv := make(map[int][]string)
	//以csv文件第一列为KEY，第二列为value，转换为map;重复时后者覆盖前者
	for i, val := range record {
		if i == 0 {
			continue
		}
		mapCsv[i] = val
	}
	return mapCsv
}
