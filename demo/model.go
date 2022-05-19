package main

import (
	"fmt"
	"github.com/datadog/go-python3"
	"os"
)

func init() {
	python3.Py_Initialize()
	if !python3.Py_IsInitialized() {
		fmt.Println("Error initializing the python interpreter!")
		os.Exit(1)
	}
}

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

// InsertBeforeSysPath
// @Description: 添加site-packages路径即包的查找路径
// @param p
func insertBeforeSysPath(p string){
	sysModule := python3.PyImport_ImportModule("sys")
	path := sysModule.GetAttrString("path")
	python3.PyList_Append(path, python3.PyUnicode_FromString(p))
}

// ImportModule
// @Description: 倒入一个包
// @param dir
// @param name
// @return *python3.PyObject
func importModule(dir, name string) *python3.PyObject {
	sysModule := python3.PyImport_ImportModule("sys") 	// import sys
	path := sysModule.GetAttrString("path")            // path = sys.path
	python3.PyList_Insert(path, 0, python3.PyUnicode_FromString(dir)) // path.insert(0, dir)
	return python3.PyImport_ImportModule(name)            // return __import__(name)
}

// pythonRepr
// @Description: PyObject转换为string
// @param o
// @return string
// @return error
func pythonRepr(o *python3.PyObject) (string, error) {
	if o == nil {
		return "", fmt.Errorf("object is nil")
	}
	s := o.Repr()
	if s == nil {
		python3.PyErr_Clear()
		return "", fmt.Errorf("failed to call Repr object method")
	}
	defer s.DecRef()

	return python3.PyUnicode_AsUTF8(s), nil
}

// PrintList
// @Description: 输出一个List
// @param list
// @return error
func printList(list *python3.PyObject) error {
	if exc := python3.PyErr_Occurred(); list == nil && exc != nil {
		return fmt.Errorf("Fail to create python list object")
	}
	defer list.DecRef()
	repr, err := pythonRepr(list)
	if err != nil {
		return fmt.Errorf("fail to get representation of object list")
	}
	fmt.Printf("python list: %s\n", repr)
	return nil
}
