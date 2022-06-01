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
```