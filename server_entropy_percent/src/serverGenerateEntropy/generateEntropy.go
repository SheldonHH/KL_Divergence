package singapore

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
	"reflect"
	"strings"
)

type dict map[string]map[string]interface{}

func GenerateEntropy(gauss_user_list string) string {
	user_list := "user1 user2"
	generate_entropy_path := "/root/KL_Divergence/data/server_joint/consolidated/calculate_entropy_golang.py"
	cmd1 := exec.Command("python3", generate_entropy_path, user_list)
	executeCmd(cmd1)
	entropysum_percent_map := obtainMapfromJson("/root/KL_Divergence/data/server_joint/consolidated/consolidated_entropysum_percent.json")
	for _, m := range entropysum_percent_map {
		// m is a map[string]interface.
		// loop over keys and values in the map.
		for k, v := range m {
			fmt.Println(k, "value is", v)
		}
	}
	return "GenerateEntropy success"
}

func executeCmd(cmd *exec.Cmd) string {
	cmd.Dir = "/root/KL_Divergence"
	var out bytes.Buffer
	var stderr bytes.Buffer
	cmd.Stdout = &out
	cmd.Stderr = &stderr
	err := cmd.Run()
	if err != nil {
		fmt.Println(fmt.Sprint(err) + ": " + stderr.String())
		return "singapore"
	}
	fmt.Println("Result: " + out.String())
	return "executeCmd done!"
}


func obtainMapfromJson(user_data_params_path string) (sg dict) {

	jsonFile, err := os.Open(user_data_params_path)
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
