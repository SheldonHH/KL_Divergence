def fit_multi_modal(mean_x, sigma_x, peak, y, x, counter):
    global global_params
    global gauss_index
    gauss_index = counter
    expected = ()
    for i in range(counter):
        expected = expected + (mean_x, sigma_x, peak)
    params, cov = curve_fit(multi_bimodal, x, y, expected, maxfev=500000)
    global_params = params
    # print("params: heee", params)
    print("params: lennnnnnnn", len(params))

    # MSE
    ys_for_sim = []
    for g in range(len(x1_list)):
        x_for_sim = float(decimal.Decimal(random.randrange(
            int(min(x1_list)*100), int(max(x1_list)*100)))/100)
        y_for_sim = multi_bimodal(
            x_for_sim, *params)
        ys_for_sim.append(y_for_sim)
    return calculate_MSE(z_list, ys_for_sim)
