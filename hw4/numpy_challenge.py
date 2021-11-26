import numpy as np


def generate_array_1(n, m, upper_bound=10):
    '''
    Generate ndarray with shape(n, m) from random distribution
    :param n: number of rows
    :param m: number of columns
    :param upper_bound: max possible value in ndarray
    :return: array with filled values
    '''
    return np.random.choice(a=upper_bound, size=(n, m))


def generate_array_2(n, m, lower_bound=0, upper_bound=10):
    '''
    Generate ndarray with shape(n, m) from random distribution
    :param n: number of rows
    :param m: number of columns
    :param lower_bound: min possible value in ndarray
    :param upper_bound: max possible value in ndarray
    :return: array with filled values
    '''
    arr = np.zeros((n, m))
    for i in range(n):
        for j in range(m):
            arr[i][j] = np.random.randint(lower_bound, upper_bound)
    return arr


def generate_array_3(n, m, val_type):
    '''
    Generate ndarray with shape(n, m) from random distribution
    :param n: number of rows
    :param m: number of columns
    :param val_type: type of filled values
    :return: array with filled values
    '''
    return np.empty((n, m), dtype=val_type)


def matrix_multiplication(mat_1, mat_2):
    '''
    Multiply 2 matices (numpy.ndarrays)
    :param m1: matrix with shape(m, n)
    :param m2: matrix with shape(n, k)
    :return m3: matrix with dims (m, k)
    '''
    m, k = mat_1.shape[0], mat_2.shape[1]
    mat_3 = []
    for i in range(m):
        vect = []
        for j in range(k):
            dot_product = mat_1[i, :] * mat_2[:, j]
            vect.append(dot_product.sum())
        mat_3.append(vect)
    return np.array(mat_3)


def multiplication_check(mats_list):
    '''
    Check if matrices can be multiplied in such order
    :param mats_list: list of matrices
    :return bool: True - whether all matrices are in proper order
    '''
    n_mats = len(mats_list)
    for i in range(n_mats-1):
        if mats_list[i].shape[1] != mats_list[i+1].shape[0]:
            return False
    return True


def multiply_matrices(mats_list):
    '''
    Multiply matrices (numpy.ndarrays) in the list
    :param mats_list: list of matrices
    :return: matrix or None (if matrices can not be multiplied)
    '''
    if multiplication_check(mats_list=mats_list):
        mat_1 = mats_list[0]
        for mat_2 in mats_list[1:]:
            mat_1 = matrix_multiplication(mat_1=mat_1, mat_2=mat_2)
        return mat_1
    return


def compute_2d_distance(arr_1, arr_2):
    '''
    Compute euclidean distance between 2 vectors in two-dimensional space
    :param arr_1: first ndarray with shape(1, 2)
    :param arr_2: second ndarray with shape(1, 2)
    :return: euclidean distance
    '''
    diff = (arr_1 - arr_2) ** 2
    return np.sqrt(diff.sum())


def compute_multidimensional_distance(arr_1, arr_2):
    '''
    Compute euclidean distance between 2 vectors in n-dimensional space
    :param arr_1: first ndarray with shape(1, n)
    :param arr_2: second ndarray with shape(1, n)
    :return: euclidean distance
    '''
    diff = (arr_1 - arr_2) ** 2
    return np.sqrt(diff.sum())


def compute_pair_distances(arr):
    '''
    Compute matrix of paired distances
    :param arr: two-dimensional ndarray
    :return: matrix if paired distances
    '''
    dist_matrix = []
    n_observations = arr.shape[0]
    for i in range(n_observations):
        dist_vect = [compute_multidimensional_distance(arr[i, :], arr[j, :]) for j in range(n_observations)]
        dist_matrix.append(dist_vect)
    return np.array(dist_matrix)


if __name__ == "__main__":
    arr_1 = generate_array_1(n=3, m=4, upper_bound=20)
    print('First array: ')
    print(arr_1)
    print()
    arr_2 = generate_array_2(n=3, m=5, lower_bound=10, upper_bound=30)
    print('Second array: ')
    print(arr_2)
    print()
    arr_3 = generate_array_3(n=3, m=3, val_type=int)
    print('Third array: ')
    print(arr_3)
