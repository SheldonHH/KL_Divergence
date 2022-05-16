# KL_Divergence
### Generate requirements.txt
```
pip3 install pipreqs
python3 -m  pipreqs.pipreqs . --force
```


### For GPU KL Divergence
```
sudo apt-get update
sudo apt install nvidia-cuda-toolkit
```


[preprocess.py]() read from raw data and generate trimmed_data


### 2D_KL
Compute the Kullback-Leibler divergence between two multivariate samples.
Parameters
x : 2D array (n,d)
  Samples from distribution P, which typically represents the true distribution.
y : 2D array (m,d)
  Samples from distribution Q, which typically represents the approximate distribution.
Returns
-------
out : float
  The estimated Kullback-Leibler divergence D(P||Q).

#### TL RL
```
python3 preprocess.py && python3 joint_frequency.py && python3 available_units.py  && python3 2d.py 
```