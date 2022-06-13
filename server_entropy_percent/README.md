# To Run the ServerGenerateEntropy

Input: consolidated gauss params file address
Output: entropy percentage for each user

## Required Directory Structure

```bash
data 
│   └───users_individual_gauss 
    │     user_1_features_gauss.json
    │     user_2_features_gauss.json
    │     user_3_features_gauss.json
          └───consolidated  
                         |   entropysum_percent.json  
```

## Installation

```python
cd py
pip3 isntall -r requirements.txt
```

```golang
go mod init server_entropy_percent
go mod tidy
```

## Usage

```golang
go run main.go
```