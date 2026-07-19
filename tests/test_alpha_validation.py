import numpy as np
import pandas as pd

from backtest.alpha_validation import bonferroni_correction, orthogonalize_factor


def test_bonferroni_correction_caps_at_one():
    corrected = bonferroni_correction([0.01, 0.20, 0.60])
    assert np.allclose(corrected, [0.03, 0.60, 1.00])


def test_orthogonalize_factor_removes_linear_exposures():
    x1 = np.arange(20, dtype=float)
    x2 = np.sin(x1)
    known = pd.DataFrame({"size": x1, "value": x2})
    factor = pd.Series(3 + 2 * x1 - 0.5 * x2 + np.cos(x1), name="candidate")
    residual = orthogonalize_factor(factor, known)
    assert abs(residual.corr(known["size"])) < 1e-12
    assert abs(residual.corr(known["value"])) < 1e-12
    assert abs(residual.mean()) < 1e-12
