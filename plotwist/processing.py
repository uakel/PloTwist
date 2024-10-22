"""
A submodule with lots of helper functions for processing data
"""

import numpy as np
from typing import List, Tuple, Callable

# Signal processing related functions
def moving_average(signal: np.ndarray, n: int) -> np.ndarray:
    """
    Compute the moving average of a signal with a window of size n.

    Args:
        signal: np.ndarray, input signal
        n: int, window size

    Returns:
        np.ndarray, moving average of the signal

    Remarks:
        Averaging window is made smaller at the edges of the signal.
    """

    averages = np.zeros(len(signal))
    for i in range(len(signal)):
        # Compute the bounds of the averaging window
        delta = min([i, len(signal) - (i + 1), n // 2])
        i_low = i - delta
        i_high = i + delta + 1
        # Compute the average
        averages[i] = 1 / (1 + 2 * delta) * np.sum(signal[i_low:i_high])
    return averages

# Signal distance related functions
def mean_squared_signal_distance(signal1: np.ndarray, signal2: np.ndarray) -> float:
    """
    Compute the mean squared distance between two signals.

    Args:
        signal1: np.ndarray, first signal
        signal2: np.ndarray, second signal

    Returns:
        float, mean squared distance between the signals
    """

    return np.mean((signal1 - signal2) ** 2)

def mean_absolute_signal_distance(signal1: np.ndarray, signal2: np.ndarray) -> float:
    """
    Compute the mean absolute distance between two signals.

    Args:
        signal1: np.ndarray, first signal
        signal2: np.ndarray, second signal

    Returns:
        float, mean absolute distance between the signals
    """

    return np.mean(np.abs(signal1 - signal2))

def find_best_shift(signal1: np.ndarray, signal2: np.ndarray, max_shift: int, 
                    distance: Callable = mean_squared_signal_distance) -> Tuple[int, float]:
    """
    Find the best shift to align two signals.

    Args:
        signal1: np.ndarray, first signal
        signal2: np.ndarray, second signal
        max_shift: int, maximum shift to consider

    Returns:
        int, best shift to align the signals
    """

    assert len(signal1) >= len(signal2)
    best_shift = 0
    best_distance = distance(signal1[:len(signal2)], signal2)
    for shift in range(1, max_shift + 1):
        signal1_cut = signal1[shift:shift + len(signal2)]
        d = distance(signal1_cut, signal2[:len(signal1_cut)])
        if d < best_distance:
            best_shift = shift
            best_distance = d
    return best_shift, best_distance

def multi_signal_best_shift_mean_distance(signal1: np.ndarray, signals: List[np.ndarray], 
                                          max_shift: int = 100, distance: Callable = mean_squared_signal_distance
                                          ) -> Tuple[float, List[int]]:
    """
    Compute the mean distance of multiple signals to a reference signal, when optimally shifted.
    Args:
        signal1: np.ndarray, reference signal
        signals: List[np.ndarray], list of signals to compare
        max_shift: int, maximum shift to consider. Default is 100
        distance: Callable, distance function to use

    Returns:
        float, mean distance of the signals to the reference signal
        List[int], best shifts for each signal
    """
    total_distance = 0
    totally_considered_data_points = 0
    shifts = []
    for signal in signals:
        shift, best_distance = find_best_shift(signal1, signal, max_shift, distance)
        shifts.append(shift)
        total_distance += best_distance * (len(signal) - shift)
        totally_considered_data_points += len(signal) - shift
    return total_distance / totally_considered_data_points, shifts




