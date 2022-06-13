# ServerGenerateEntropy

- Input: consolidated gauss params file address
- Output: entropy percentage for each user

## 1. Required Directory Structure

```bash
data 
│   └───users_individual_gauss 
    │     user_1_features_gauss.json
    │     user_2_features_gauss.json
    │     user_3_features_gauss.json
          └───consolidated  
                         |   entropysum_percent.json  
```

## 2. Installation

```python
cd py
pip3 isntall -r requirements.txt
```

```golang
go mod init server_entropy_percent
go mod tidy
```

## 3. Usage

```golang
go run main.go
```

## 4. Execution Explain
`main.go` will execute the following python3 file sequentially.

1. `server_consolidated_golang.py` to consolidate all users' features gausses together 

- input: 
-- `user_1_features_gauss.json`
-- `user_2_features_gauss.json`
-- `user_3_features_gauss.json`
- Output: `consolidated/consolidated_gauss_params.json`

2. `calculate_entropy_golang.py`: calculate the entropy percent based on consolidated users' gauss results 

- Input: `consolidated/consolidated_gauss_params.json`
- Output: `consolidated/entropysum_percent.json`