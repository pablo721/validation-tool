

def parse_process_cols(form):
    n_cols = max([int(item[-1]) for item in form.keys()])
    res = {}
    for i in range(1, n_cols+1):
        res[i] = {k[:-2]: v for k, v in form.items() if int(k[-1]) == i}
    return res


