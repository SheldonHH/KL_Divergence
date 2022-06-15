from tally import csv_to_jpeg
from py_torch.FeatureExtractor import extract_features
from tally import round_data_golang 
from tally import countFreq_golang
from tally import freq_to_gauss_golang

def main():
  raw_csv_argv = ["/root/KL_Divergence/user_gauss_params/data/user_2.csv"]
  raw_data_len = csv_to_jpeg.csv_to_jpeg(raw_csv_argv)
  extract_features(raw_csv_argv)
  round_data_golang.round_data(raw_csv_argv)
  countFreq_golang.count_freq(raw_csv_argv)
  freq_to_gauss_golang.freq_to_gauss(raw_csv_argv, raw_data_len)


if __name__ == "__main__":

    main()