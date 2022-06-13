package singapore

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
)

type dict map[string]map[string]interface{}

var (
	_, b, _, _ = runtime.Caller(0)
	basepath   = filepath.Dir(b)
)

func GenerateEntropy(gauss_users_dir string) string {
	consolidate_gauss_path := "server_entropy_percent/py/server_consolidate_golang.py"
	cmd1 := exec.Command("python3", consolidate_gauss_path, gauss_users_dir)
	executeCmd(cmd1)

	generate_entropy_path := "server_entropy_percent/py/calculate_entrotally.py"
	cmd2 := exec.Command("python3", generate_entropy_path, gauss_users_dir)
	executeCmd(cmd2)
	// entropysum_percent_map := obtainMapfromJson("server_entropy_percent/data/users_individual_gauss/consolidated/consolidated_entropysum_percent.json")
	// for _, m := range entropysum_percent_map {
	// 	// m is a map[string]interface.
	// 	// loop over keys and values in the map.
	// 	for k, v := range m {
	// 		fmt.Println(k, "value is", v)
	// 	}
	// }
	return "GenerateEntropy success"
}

func executeCmd(cmd *exec.Cmd) string {
	exclude_last := basepath[0:strings.LastIndex(basepath, "/")]
	exclude_second_last := exclude_last[0:strings.LastIndex(exclude_last, "/")]
	cmd.Dir = exclude_second_last
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
