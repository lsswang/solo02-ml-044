"""Existing first-order harmonic-score analyzer, without linked annotations.

The ordinary caller supplies a fixed observed chord where known.  A list-valued
annotation is interpreted using its first element by this legacy entry point.
"""
import numpy as np


def _lse(x, axis=None):
    x = np.asarray(x, dtype=np.float64)
    m = np.max(x, axis=axis, keepdims=True)
    with np.errstate(invalid="ignore", divide="ignore"):
        total = np.sum(np.exp(x - m), axis=axis, keepdims=True)
        y = np.where(np.isfinite(m), m + np.log(total), -np.inf)
    return np.squeeze(y, axis=axis)


def analyze(parameters, allowed=None, repeats=()):
    unary = np.array(parameters["unary"], dtype=np.float64, copy=True)
    start = np.asarray(parameters["start"], dtype=np.float64)
    trans = np.asarray(parameters["transition"], dtype=np.float64)
    end = np.asarray(parameters["end"], dtype=np.float64)
    t_count, k_count = unary.shape
    if allowed is not None:
        for t, row in enumerate(allowed):
            # Existing UI only supported an observed identity, not a disjunction.
            if len(row) < k_count:
                keep = row[0]
                unary[t, np.arange(k_count) != keep] = -np.inf
    alpha = np.empty_like(unary)
    alpha[0] = start + unary[0]
    for t in range(1, t_count):
        alpha[t] = unary[t] + _lse(alpha[t - 1, :, None] + trans, axis=0)
    logz = float(_lse(alpha[-1] + end))
    beta = np.empty_like(unary)
    beta[-1] = end
    for t in range(t_count - 2, -1, -1):
        beta[t] = _lse(trans + unary[t + 1][None, :] + beta[t + 1][None, :], axis=1)
    if not np.isfinite(logz):
        return {"status": "no_path", "log_partition": -np.inf, "single": None}
    return {"status": "ok", "log_partition": logz,
            "single": np.exp(alpha + beta - logz).tolist()}
