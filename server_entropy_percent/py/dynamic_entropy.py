from tally import server_consolidate_golang
from tally import calculate_entropy_golang 

def main():
  individual_gauss = ["/root/KL_Divergence/server_entropy_percent/data/users_individual_gauss"] # location where stores individual gauss
  users_list = ["user_1", "user_2", "user_4"]
  server_consolidate_golang.server_consolidate(individual_gauss,users_list)
  calculate_entropy_golang.calculate_entropy(individual_gauss)


if __name__ == "__main__":
    main()