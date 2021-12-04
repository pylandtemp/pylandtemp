from .algorithms import (
    ComputeMonoWindowEmissivity,
    ComputeEmissivityNBEM,
    ComputeEmissivityGopinadh,
)

default_algorithms = {
    "avdan": ComputeMonoWindowEmissivity,
    "xiaolei": ComputeEmissivityNBEM,
    "gopinadh": ComputeEmissivityGopinadh,
}
