# Copyright (c) 2020, NVIDIA CORPORATION.

from cuspatial._lib.interpolate import (
    cubicspline_full
)

from cudf import DataFrame
from cudf.core.index import RangeIndex

def cubic_spline_2(x, y, ids, prefix_sums):
    """
    Fits each column of the input DataFrame `y` to a hermetic cubic spline.

    Parameters
    ----------
    x : cudf.Series
        time sample values. Must be monotonically increasing.
    y : cudf.DataFrame
        columns to have curves fit to according to x
    ids_and_end_coordinates: cudf.DataFrame
                             ids and final positions of each set of
                             trajectories

    Returns
    -------
    m x n DataFrame of trajectory curve coefficients.
    m is len(ids_and_end_coordinates), n is 4 * len(y.columns)
    """
    x_c = x._column
    y_c = y._column
    ids_c = ids._column
    prefix_c = prefix_sums._column
    result_table = cubicspline_full(x_c, y_c, ids_c, prefix_c)
    result_table._index = RangeIndex(result_table._num_rows)
    result = DataFrame._from_table(result_table)
    return result
