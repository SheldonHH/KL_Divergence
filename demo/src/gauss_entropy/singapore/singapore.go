package singapore

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
	"bytes"
	"reflect"
	"strings"
)

type dict map[string]map[string]interface{}

// // https://stackoverflow.com/a/15815730/5772735
// func GenerateGauss(raw_data_path string) (string){
// 	// string raw_data_path = "/root/KL_Divergence/data_sample/user_1_data.csv"
// 	trim_data_path := "/root/KL_Divergence/preprocess_golang.py"
// 	independent_freq_path := "/root/KL_Divergence/indepenedent_frequency_golang.py"
// 	generate_gauss_path := "/root/KL_Divergence/generate_gauss_golang.py"

// 	// out, err := exec.Command("python3",trim_data_path, raw_data_path).Output()
// 	// if err != nil {
// 	// 	log.Fatal(err)
// 	// }
// 	// fmt.Printf("The date is %s\n", out)
// 	// return string(out)

// 	// set current working directory
// 	mydir, err1 := os.Getwd()
// 	if err1 != nil {
// 			fmt.Println(err1)
// 	}
// 	fmt.Println(mydir)
// 	cmd1 := exec.Command("python3",trim_data_path, raw_data_path)
// 	cmd2 := exec.Command("python3",independent_freq_path, raw_data_path)
// 	cmd3 := exec.Command("python3",generate_gauss_path, raw_data_path)
// 	cmd1.Dir,cmd2.Dir,cmd3.Dir = "/root/KL_Divergence","/root/KL_Divergence","/root/KL_Divergence"
// 	out1, err1 := cmd1.Output()
// 	if err1 != nil {
// 		fmt.Println(fmt.Sprint(err1))
// 		return "err1"
// 	}
// 	fmt.Println(string(out1))

// 	out2, err2 := cmd2.Output()
// 	if err2 != nil {
// 		fmt.Println(fmt.Sprint(err2))
// 		return "err2"
// 	}
// 	fmt.Println(string(out2))

// 	out3, err3 := cmd3.Output()
// 	if err3 != nil {
// 		fmt.Println(fmt.Sprint(err3))
// 		return "err3"
// 	}
// 	fmt.Println(string(out3))
// 	// https://stackoverflow.com/a/15815730/5772735    Answer recommended by Go Language

// 	return "success"

// }

func GenerateEntropy(gauss_user_list string) string{
	user_list := "user1 user2"
	generate_entropy_path := "/root/KL_Divergence/data/joint/consolidated/calculate_entropy_golang.py"
	cmd1 := exec.Command("python3",generate_entropy_path, user_list)
	executeCmd(cmd1)
	entropysum_percent_map := obtainMapfromJson("/root/KL_Divergence/data_sample/joint/consolidated/consolidated_entropysum_percent.json")
	for _, m := range entropysum_percent_map {
    // m is a map[string]interface.
    // loop over keys and values in the map.
    for k, v := range m {
        fmt.Println(k, "value is", v)
    }
	}
	return "GenerateEntropy success"
}

// https://stackoverflow.com/a/15815730/5772735
func GenerateGauss(raw_data_path string) (string){
	// string raw_data_path = "/root/KL_Divergence/data_sample/user_1_data.csv"
	trim_data_path := "/root/KL_Divergence/preprocess_golang.py"
	independent_freq_path := "/root/KL_Divergence/independent_frequency_golang.py"
	generate_gauss_path := "/root/KL_Divergence/generate_gauss_golang.py"
	cmd1 := exec.Command("python3",trim_data_path, raw_data_path)
	fmt.Println("cmd1 = ", reflect.TypeOf(cmd1))
	cmd2 := exec.Command("python3",independent_freq_path, raw_data_path)
	cmd3 := exec.Command("python3",generate_gauss_path, raw_data_path)
	executeCmd(cmd1)
	executeCmd(cmd2)
	executeCmd(cmd3)

	// read result gauss params json from file
	forward_slash := strings.LastIndex(raw_data_path,"/")
	dot_index := strings.LastIndex(raw_data_path,".")
	first_half := string(raw_data_path[0:forward_slash])
	file_name_without_extension := string(raw_data_path[forward_slash:dot_index])
	user_data_params_path := first_half + "/joint" + file_name_without_extension+"_params.json"
	gauss_map_one_user := obtainMapfromJson(user_data_params_path)

	fmt.Println("user_data_params_path",user_data_params_path)

	for _, m := range gauss_map_one_user {
    // m is a map[string]interface.
    // loop over keys and values in the map.
    for k, v := range m {
        fmt.Println(k, "value is", v)
    }
	}
	return "success"
}

func executeCmd(cmd *exec.Cmd) string{
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


// func generateEntropies(raw_data_path string) (sg dict) {
// 	string entropies = "/root/KL_Divergence/generate_gauss_golang.py"
// 	exec.Command()
// 	exec.Command("../data_sample/joint/consolidated/calculate_entropy.py").Run()

// 	jsonFile, err := os.Open(jsonStrPath)
// 	if err != nil {
// 		fmt.Println(err)
// 	}
// 	fmt.Println("Successfully Opened users.json")
// 	// defer the closing of our percent_jsonFile so that we can parse it later on
// 	defer jsonFile.Close()
// 	byteValue, _ := ioutil.ReadAll(jsonFile)
// 	var result map[string]map[string]interface{}
// 	json.Unmarshal([]byte(byteValue), &result)
// 	sg = result
// 	return
// }



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



// code for debug https://stackoverflow.com/a/15815730/5772735    Answer recommended by Go Language
	// var out bytes.Buffer
	// var stderr bytes.Buffer
	// cmd.Stdout = &out
	// cmd.Stderr = &stderr
	// err := cmd.Run()
	// if err != nil {
	// 		fmt.Println(fmt.Sprint(err) + ": " + stderr.String())
	// 		return "singapore"
	// }
	// fmt.Println("Result: " + out.String())