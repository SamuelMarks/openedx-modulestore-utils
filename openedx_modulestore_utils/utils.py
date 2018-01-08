def update_d(d, arg=None, **kwargs):
    if arg:
        d.update(arg)
    if kwargs:
        d.update(kwargs)
    return d


def set_update_d(d, k, v):
    if k in d:
        d[k].update(v)
    else:
        d[k] = v
    return d
