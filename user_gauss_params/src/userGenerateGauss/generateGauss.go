package userGenerateGauss

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

func GenerateGauss(raw_data_path string) string {
	trim_data_path := "user_gauss_params/py/preprocess_golang.py"
	independent_freq_path := "user_gauss_params/py/independent_frequency_golang.py"
	generate_gauss_path := "user_gauss_params/py/generate_gauss_golang.py"
	cmd1 := exec.Command("python3", trim_data_path, raw_data_path)
	fmt.Println("cmd1 = ", reflect.TypeOf(cmd1))
	cmd2 := exec.Command("python3", independent_freq_path, raw_data_path)
	cmd3 := exec.Command("python3", generate_gauss_path, raw_data_path)
	executeCmd(cmd1)
	executeCmd(cmd2)
	executeCmd(cmd3)

	forward_slash := strings.LastIndex(raw_data_path, "/")
	dot_index := strings.LastIndex(raw_data_path, ".")
	first_half := string(raw_data_path[0:forward_slash])
	file_name_without_extension := string(raw_data_path[forward_slash:dot_index])
	user_data_params_path := first_half + "/gauss_result" + file_name_without_extension + "_params.json"
	gauss_map_one_user := obtainMapfromJson(user_data_params_path)

	fmt.Println("user_data_params_path", user_data_params_path)

	for _, m := range gauss_map_one_user {
		for k, v := range m {
			fmt.Println(k, "value is", v)
		}
	}
	return "success"
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
