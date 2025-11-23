from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass
class ClassificationResult:
    label: str
    stability: str
    delta: float
    markdown: str


@dataclass(frozen=True)
class AppConfig:
    tr_min: float = -10.0
    tr_max: float = 10.0
    det_min: float = -10.0
    det_max: float = 30.0
    grid_res: int = 800
    eps: float = 1e-8
