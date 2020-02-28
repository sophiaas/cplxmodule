# Real- and Complex- valued Variational Dropout

## Usage

### Collecting KL divergence terms

The variational dropout and relevance determination techniques require a penalty term to be introduced to the loss objective. The term is given by the Kullback-Leibler divergences of the variational approximation from the assumed prior distribution.

Each layer, which inherits from `BaseARD`, is responsible for computing the KL divergence terms related to the variational approximations of and only its own parameters, e.g. children submodules in turn compute their own divergences. Therefore the layer must implement a the `.penalty` read-only property, which is responsible for computing the divergence.

The following functions return generators, that yield the penalties of all eligible submodules.

* `named_penalties(module, reduction="sum", prefix='')` much like the `.named_modules` method of any pytorch Module, this generator yields submodule's name and penalty value pairs. The penalty values are taken from `.penalty` and reduced, depending on the `reduction` setting.

* `penalties(module, reduction="sum")` the same as `named_penalties()` but yield the penalty values only. Handy if one needs short loss expression:

```python
from cplxmodule.nn.relevance import penalties

loss = criterion(model(X), y) + coef * sum(penalties(model, reduction="sum"))
```

### Computing relevance masks

The variational dropout and relevance determination methods use special Fully Factorised Gaussian approximation with mean `\mu` and variance `\alpha \lvert \mu \rvert^2`. The `\alpha` is essentially the ratio of mean to standard deviation and is learnt either directly, or through a additive reparameterization. It effectively scores the irrelevance of the parameter it is associated with: `\alpha` is close to zero, then the parameter is more relevant, rather than the parameter with `\alpha` above `1`.

In order to decide if a parameter is relevant it is necessary to compare its irrelevance score against a threshold. The following functions can be used for returning the masks of kept/dropped out (sparsified) parametersL

* `named_relevance(module, threshold=..., hard=True)` much like the `.named_penalties`, this generator yields submodule's name and the computed relevance mask, which is `nonzero` at those parameter elements, which have `\log\alpha` below the given `threshold`. `hard` forces the returend mask to be binary.

* `compute_ard_masks(module, threshold=..., hard=True)` also returns the sparsity mask, but unlike `named_relevance` returns a dictionary of masks, keyed by parameter manes compatible with the masking interface of the layers in `nn.masked`.

### Transferring learn weights from non-variational modules

Since variational approximations use additive noise reparameterization, each
variational dropout module in `nn.relevance`

## Implementation

### Modules

The modules in `nn.relevance` implement both `real`- and `complex` valued variational dropout methods. Due to poor naming, used in earlier version of the library the naming of variational dropout method and automatic relevance determination were mixed up. As of *2020-02-28* the naming in `nn.relevance.real` and `nn.relevance.complex`  must be disregarded and correctly named real and complex valued layers must be imported from `nn.relevance.extensions`.

* Variational dropout (log-uniform prior)
    - (real) LinearVD, Conv1dVD, Conv2dVD, BilinearVD
    - (complex) CplxLinearVD, CplxConv1dVD, CplxConv2dVD, CplxBilinearVD

* Automatic Relevance Determination (log-uniform prior)
    - (real) LinearARD, Conv1dARD, Conv2dARD, BilinearARD
    - (complex) CplxLinearARD, CplxConv1dARD, CplxConv2dARD, CplxBilinearARD

* Variational dropout with bogus forward values but exact gradients
    - (complex only) CplxLinearVDBogus, CplxConv1dVD, CplxConv2dVD, CplxBilinearVD

### Subclassing Modules

Since `BaseARD` does not have `__init__`, it can be placed anywhere in the list of base classes in the definition, when subclassing or multiply inheriting from `BaseARD`.

## Compatibility

As of 2020-02-28 the modules and their API was designed so as to comply with the public interface exposed in pytorch 1.4.