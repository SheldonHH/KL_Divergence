### 高斯模拟，传入：private data，传出Gaussian模拟结果
user_gauss_params
### contribution：所有用户Gaussian模拟的结果，传出每一个user的占所有的那个比例
server_entropy_percent

```
go mod init <module_name>
go mod tidy
```

```
git filter-branch -f  --prune-empty --index-filter 'git rm -rf --cached --ignore-unmatch user_gauss_params/data/uneven/user_4.txt' --tag-name-filter cat -- --all
git filter-branch -f  --prune-empty --index-filter 'git rm -rf --cached --ignore-unmatch user_gauss_params/data/uniform/uniform/user_2_mnist_Xtrain.csv' --tag-name-filter cat -- --all
git filter-branch -f  --prune-empty --index-filter 'git rm -rf --cached --ignore-unmatch user_gauss_params/data/uniform/uniform/user_1_mnist_Xtrain_.csv' --tag-name-filter cat -- --all
git filter-branch -f  --prune-empty --index-filter 'git rm -rf --cached --ignore-unmatch user_gauss_params/data/uniform/uniform/user_3_mnist_Xtrain.csv' --tag-name-filter cat -- --all
git filter-branch -f  --prune-empty --index-filter 'git rm -rf --cached --ignore-unmatch user_gauss_params/data/uniform/uniform/user_4_mnist_Xtrain.csv' --tag-name-filter cat -- --all

git filter-branch -f  --prune-empty --index-filter 'git rm -rf --cached --ignore-unmatch user_gauss_params/data/uniform/features/freq/test.txt' --tag-name-filter cat -- --all

```

git filter-branch -f  --prune-empty --index-filter 'git rm -rf --cached --ignore-unmatch ./user_gauss_params/py/test.txt' --tag-name-filter cat -- --all
git filter-branch -f  --prune-empty --index-filter 'git rm -rf --cached --ignore-unmatch ./user_gauss_params/data/uniform/uniform/user_3_mnist_Xtrain.csv' --tag-name-filter cat -- --all
git filter-branch -f  --prune-empty --index-filter 'git rm -rf --cached --ignore-unmatch ./user_gauss_params/data/uniform/uniform/user_4_mnist_Xtrain.csv' --tag-name-filter cat -- --all
git filter-branch -f  --prune-empty --index-filter 'git rm -rf --cached --ignore-unmatch ./user_gauss_params/data/uniform/uniform/user_2_mnist_Xtrain.csv' --tag-name-filter cat -- --all
git filter-branch -f  --prune-empty --index-filter 'git rm -rf --cached --ignore-unmatch ./user_gauss_params/data/uniform/uniform/user_4_mnist_Xtrain.csv' --tag-name-filter cat -- --all
git filter-branch -f  --prune-empty --index-filter 'git rm -rf --cached --ignore-unmatch ./user_gauss_params/data/uniform/uniform/user_1_mnist_Xtrain.csv' --tag-name-filter cat -- --all
git filter-branch -f  --prune-empty --index-filter 'git rm -rf --cached --ignore-unmatch ./user_gauss_params/data/uniform/user_4.txt' --tag-name-filter cat -- --all
git filter-branch -f  --prune-empty --index-filter 'git rm -rf --cached --ignore-unmatch ./user_gauss_params/data/uniform/user_3.txt' --tag-name-filter cat -- --all
git filter-branch -f  --prune-empty --index-filter 'git rm -rf --cached --ignore-unmatch ./user_gauss_params/data/uniform/user_1.txt' --tag-name-filter cat -- --all
git filter-branch -f  --prune-empty --index-filter 'git rm -rf --cached --ignore-unmatch user_gauss_params/data/uniform/features/freq/test.txt' --tag-name-filter cat -- --all

rm ./user_gauss_params/py/test.txt
rm ./user_gauss_params/data/uniform/uniform/user_3_mnist_Xtrain.csv
rm ./user_gauss_params/data/uniform/uniform/user_4_mnist_Xtrain.csv
rm ./user_gauss_params/data/uniform/uniform/user_2_mnist_Xtrain.csv
rm ./user_gauss_params/data/uniform/uniform/user_1_mnist_Xtrain_.csv
rm ./user_gauss_params/data/uniform/user_4.txt
rm ./user_gauss_params/data/uniform/user_1.txt
rm ./user_gauss_params/data/uniform/user_3.txt
rm ./user_gauss_params/data/uniform/user_2.txt

