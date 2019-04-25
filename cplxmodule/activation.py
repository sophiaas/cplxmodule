import torch
import torch.nn

import torch.nn.functional as F

from .base import CplxToCplx, CplxToReal

from .cplx import cplx_modulus, cplx_angle
from .cplx import cplx_apply, cplx_exp, cplx_log


class CplxActivation(CplxToCplx):
    r"""
    Applies the function elementwise passing positional and keyword arguments.
    """
    def __init__(self, f, *a, **k):
        super().__init__()
        self.f, self.a, self.k = f, a, k

    def forward(self, input):
        return cplx_apply(input, self.f, *self.a, **self.k)


class CplxModulus(CplxToReal):
    def forward(self, input):
        return cplx_modulus(input)


class CplxAngle(CplxToReal):
    def forward(self, input):
        return cplx_angle(input)


class CplxIdentity(CplxToCplx):
    def forward(self, input):
        return input


class CplxExp(CplxToCplx):
    def forward(self, input):
        return cplx_exp(input)


class CplxLog(CplxToCplx):
    def forward(self, input):
        return cplx_log(input)