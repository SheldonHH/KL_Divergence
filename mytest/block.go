package main

type update struct {
	senderID string //who generates the new update
	summary string //data summary of private data
	signature string //signature obtain after data verification
	epochNum int //height of epoch
	params[2] float32 //updates of weights
}

type block struct {

}
