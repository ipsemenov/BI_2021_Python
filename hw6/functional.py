def chech_args_availability(*args):
    '''
    Accepts an arbitary number of arguments and check their availability:
    their number should be more than 2 and the last argument should be a list.
    If arguments does not satisfy these conditions, it raise an error.
    :param args: positional arguments
    '''
    if len(args) < 2:
        raise AssertionError('You should pass at least 2 argumnets into function: function name and list object')
    if not isinstance(args[-1], list):
        raise AssertionError('Last argument should be a list object')


def sequential_map(*args):
    '''
    Accepts an arbitary number of functions and list object as the last argument.
    Then consistently applies these functions to list.
    :param args: arbitary number of functions and list object as the last argument
    :return: modified list
    '''
    # checking arguments availability
    chech_args_availability(*args)

    funcs = args[:-1]
    lst = args[-1]
    lst = func_chain(*funcs)(lst)

    # convert result to list object
    if not isinstance(lst, list):
        lst = list(lst)

    # round float values if all of them have a zero after point
    if all([numb.is_integer() for numb in lst]):
        lst = list(map(int, lst))

    return lst


def consensus_filter(*args):
    '''
    Accepts an arbitary number of bool functions and list object as the last argument.
    Then consistently applies these functions to list and return those elements of the list
    which gave True after applying each of the functions
    :param args: arbitary number of bool functions and list object as the last argument
    :return: a slice of the original list
    '''

    # checking arguments availability
    chech_args_availability(*args)

    funcs = args[:-1]
    lst = args[-1]
    for func in funcs:
        lst = list(filter(func, lst))

    return lst


def conditional_reduce(func_1, func_2, lst):
    '''
    Accepts two functions and list object.
    First function filters elements of the list and returns slice of the original list.
    Second function accepts these elements and does some manipulations with them returning one value.
    :param func_1: bool function which accepts arbitary number of arguments
    :param func_2: function which accepts slice of the original list and returns single value
    :return: single value
    '''
    filtered_args = list(filter(func_1, lst))
    return func_2(*filtered_args)


def func_chain(*funcs):
    '''
    Accepts an arbitary number of bool functions and integrate them into one function
    :param funcs: arbitary number of functions
    :return: some value(s) - result of consistent application of passed functions
    '''
    def wrapper_around_func_chain(args):
        '''
        Wrapper around func_chain function. Makes consistent application of functions
        passed into decorator function - func_chain.
        :param args: positional arguments
        :return: function which is a result of consistent application of passed functions
        '''
        for func in funcs:
            args = func(args)
        return args
    return wrapper_around_func_chain


def multiple_partial(*funcs, **kwargs):
    '''
    Accepts an arbitary number of functions and keyword arguments for them.
    It “freezes” some portion of a function’s keyword arguments resulting in a new object
    with a simplified signature.
    :param funcs: list of functions
    :kwargs: keyword arguments
    :return: list of functions
    '''
    def partial(func, *args, **kwargs):
        def newfunc(*fargs, **fkwargs):
            newkwargs = kwargs.copy()
            newkwargs.update(fkwargs)
            return func(*fargs, **newkwargs)
        return newfunc
    new_funcs = []
    for func in funcs:
        new_funcs.append(partial(func, **kwargs))
    return new_funcs
