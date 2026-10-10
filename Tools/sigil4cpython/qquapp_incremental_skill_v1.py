# SPDX-License-Identifier: MIT
"""Explicitly calibrated, opt-in scikit-learn learner for QQUAPP skill source.

Preparation is frozen before learning, so later partial_fit batches do not
silently change the linear model's feature coordinate system.
Prediction is advice, not UAP authorization or an action in PACA.IO.
No pickle/joblib/network/persistence or implicit training occurs on import.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Sequence


@dataclass(frozen=True)
class Advisory:
    labels: tuple[str, ...]
    schema_id: str
    occurrence: str
    verdict: str = "PREDICTION_ONLY"
    decision_authority: bool = False
    external_effect: bool = False
    uap: str = "UNJUDGED"


class IncrementalSkill:
    """Finite feature schema and fixed class vocabulary, incremental SGD classifier.

    If scikit-learn is unavailable, instantiate fails with an explicit
    ImportError. A QUNO-facing interface may convert that to HOLD_QUNO.
    """

    def __init__(self, *, features: tuple[str, ...], classes: tuple[str, ...],
                 occurrence: str, random_state: int = 42):
        if (not features or not classes or len(classes) < 2 or
                len(set(features)) != len(features) or
                len(set(classes)) != len(classes) or
                any(not x or not isinstance(x, str) for x in features + classes)):
            raise ValueError("INVALID_TYPED_FEATURES_OR_CLASSES")
        if not occurrence or not isinstance(occurrence, str):
            raise ValueError("OCCURRENCE_REQUIRED")
        if type(random_state) is not int:
            raise ValueError("FIXED_INTEGER_SEED_REQUIRED")
        try:
            import numpy as np
            from sklearn.preprocessing import StandardScaler
            from sklearn.linear_model import SGDClassifier
        except ImportError as exc:
            raise ImportError("HOLD_QUNO:SCIKit_LEARN_DEPENDENCY_UNAVAILABLE") from exc
        self._np = np
        self.features = features
        self.classes = classes
        self.occurrence = occurrence
        self.scaler = StandardScaler()
        self.classifier = SGDClassifier(loss="log_loss", random_state=random_state)
        self.calibrated = False
        self.trained = False
        self.batches = 0
        self._train_epoch = 0

    def _rows(self, X: Sequence[Sequence[float]]):
        arr = self._np.asarray(X, dtype=float)
        if (arr.ndim != 2 or arr.shape[0] == 0 or
                arr.shape[1] != len(self.features) or not self._np.isfinite(arr).all()):
            raise ValueError("INVALID_FINITE_FEATURE_MATRIX")
        return arr

    def calibrate(self, X: Sequence[Sequence[float]]) -> None:
        if self.calibrated:
            raise ValueError("SCALER_FROZEN_NEW_CALIBRATION_REQUIRES_NEW_OCCURRENCE")
        arr = self._rows(X)
        self.scaler.partial_fit(arr)
        self.calibrated = True

    def learn(self, X: Sequence[Sequence[float]], y: Sequence[str], *,
              epoch: int) -> str:
        if not self.calibrated:
            return "HOLD_QUNO:SCALER_NOT_CALIBRATED"
        if type(epoch) is not int or epoch != self._train_epoch + 1:
            return "HOLD_QUNO:NONFRESH_EPOCH"
        arr = self._rows(X)
        if len(y) != len(arr) or any(label not in self.classes for label in y):
            raise ValueError("INVALID_LABEL_BATCH")
        scaled = self.scaler.transform(arr)
        if not self.trained:
            self.classifier.partial_fit(scaled, y, classes=self._np.array(self.classes))
        else:
            self.classifier.partial_fit(scaled, y)
        self.trained = True
        self._train_epoch = epoch
        self.batches += 1
        return "ADMIT_SOURCE_PLAN:MODEL_UPDATED_IN_MEMORY"

    def advise(self, X: Sequence[Sequence[float]]) -> Advisory:
        if not self.trained:
            raise ValueError("QUNO:MODEL_NOT_TRAINED")
        arr = self._rows(X)
        values = self.classifier.predict(self.scaler.transform(arr))
        return Advisory(tuple(str(x) for x in values),
                        schema_id="SIGIL_QQUAPP_TRANSFERABLE_SKILL_PULL_PUSH_V1",
                        occurrence=self.occurrence)
