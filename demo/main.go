package main

import (
	"encoding/csv"
	"io/ioutil"
	"log"
	"strings"
	"fmt"
	"github.com/datadog/go-python3"
)


//调用Python实现model training
func modelTraining(privateData map[int][]string) update {
	var newUpdate update
	newUpdate.signature = "U0-signature"
	newUpdate.senderID = "U0"
	newUpdate.epochNum = 1
	newUpdate.summary = "U0-data-summary"

	params := [2]float32{0.1,0.1}
	//设置本地python import路径
	py37 := "/Users/fiona/anaconda3/envs/python37/lib/python3.7/site-packages"
	insertBeforeSysPath(py37)

	hello := importModule("./py", "hello")

	helloRepr, err := pythonRepr(hello)
	if err != nil {
		panic(err)
	}
	fmt.Printf("[MODULE] repr(hello) = %s\n", helloRepr)
	// 4. 获取变量
	a := hello.GetAttrString("a")
	aString, err := pythonRepr(a)
	if err != nil {
		panic(err)
	}
	fmt.Printf("[VARS] a = %#v\n", aString)
	// 5. 获取函数方法
	sayHello := hello.GetAttrString("sayHello")
	// 设置调用的参数（一个元组）
	args := python3.PyTuple_New(1)	// 创建存储空间
	python3.PyTuple_SetItem(args, 0, python3.PyUnicode_FromString("xwj"))	// 设置值
	res := sayHello.Call(args, python3.Py_None)	// 调用
	fmt.Printf("[FUNC] res = %s\n", python3.PyUnicode_AsUTF8(res))
	// 6. 调用第三方库sklearn
	sklearn := hello.GetAttrString("sklearn")
	skVersion := sklearn.GetAttrString("__version__")
	sklearnRepr, err := pythonRepr(sklearn)
	if err != nil {
		panic(err)
	}
	skVersionRepr, err := pythonRepr(skVersion)
	if err != nil {
		panic(err)
	}
	fmt.Printf("[IMPORT] sklearn = %s\n", sklearnRepr)
	fmt.Printf("[IMPORT] sklearn version =  %s\n", skVersionRepr)
	//7. 结束环境
	python3.Py_Finalize()

	newUpdate.params = params
	return newUpdate
}


func main() {
	dataPath := "data/U0_data.csv"
	privateData := readPrivateData(dataPath)
	fmt.Println(privateData)
	// newUpdate := modelTraining(privateData)
	// fmt.Println(newUpdate.senderID)
}

func readPrivateData(filePath string) map[int][]string { //用户读取私人数据
	dat, err := ioutil.ReadFile(filePath)
	if err != nil {
		log.Fatal(err)
	}
	r := csv.NewReader(strings.NewReader(string(dat[:])))

	record, err := r.ReadAll()  //record为与CSV同样结构的二维数组
	if err != nil {
		panic("Fail to read csv file!")
	}
	mapCsv := make(map[int][]string)
	//以csv文件第一列为KEY，第二列为value，转换为map;重复时后者覆盖前者
	for i, val := range record {
		if i ==0 {
			continue
		}
		mapCsv[i] = val
	}
	return mapCsv
}