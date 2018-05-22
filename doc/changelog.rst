Changelog
=========
DecoTengu 0.14.1
----------------
- carefully account for floating point inaccuracy when calculating ascent
  and first decompression stop

DecoTengu 0.14.0
----------------
- fixed first stop decompression algorithm to not ignore ascent target

DecoTengu 0.13.0
----------------
- change algorithm calculating length of decompression stop to check ascent
  ceiling limit without ascending to next decompression stop; this makes
  total decompression time of a dive longer by about 1 minute, but takes
  the same approach towards close ascent ceiling limit as in case of default
  first decompression stop search; it also boosts performance of the
  algorithm

DecoTengu 0.12.0
----------------
- first decompression stop validator improvements

DecoTengu 0.11.0
----------------
- use exponential function group homomorphism ``exp(x + y) = exp(x) * exp(y)``
  to reimplement tabular calculator
- above forced redesign of decompression model code with API changes

  - ``TissueCalculator`` class is removed
  - ``eq_schreiner`` function is removed
  - ``TabTissueCalculator`` class is replaced with ``TabExp`` class and all
    other classes and functions related to tabular calculations are
    removed including tabular first decompression stop finder

- the overall redesign of decompression model and tabular calculations code

  - is much simpler with 10% lines of overall codebase removed
  - uses less memory for tabular calculations
  - boosts performance of basic decompression engine by 20% and tabular
    based decompression engine by almost 300%

- changed all methods and functions to accept time in minutes instead of
  time in seconds

DecoTengu 0.10.0
----------------
- implemented new, faster and simpler algorithm finding first decompression
  stop
- old algorithm finding first decompression stop, based on binary search,
  moved to decotengu.alt.bisect module as it still can be used for comparison
  purposes

DecoTengu 0.9.0
---------------
- memory usage improvements
- API change: decompression table is ``Engine.deco_table`` attribute
  instead of being a coroutine

DecoTengu 0.8.0
---------------
- implemented tabular tissue saturation calculator to allow decompression
  calculations without exponential function
- implemented naive algorithm calculating length of decompression stop
  using 1 minute interval; to be used for comparison purposes only
- implemented initial support for calculations with decimal data type
- various performance improvements

DecoTengu 0.7.0
---------------
- added documentation section about algorithms related to dive ascent
- various bug fixes

DecoTengu 0.6.0
---------------
- dive time changed to be dive bottom time (includes descent time)
- allow to configure last decompression stop at 6m
- various bug fixes
- API changes

  - added new dive phase ``GAS_MIX`` to allow identify gas mix switch easily
  - ``DECOSTEP`` dive phase renamed to ``DECO_STEP``
  - ``ZH_L16_GF.pressure_limit`` renamed to ``ZH_L16_GF.ceiling_limit``

- internal API changes

  - ``Engine._inv_ascent`` renamed to ``Engine._inv_limit``
  - ``Engine._inv_deco_stop`` accepts ``time`` parameter to enable
    last decompression stop at 6m
  - ``Engine._deco_ascent`` replaced with ``Engine._deco_stop``, the latter
    method does not perform any ascent anymore, just calculates
    decompression stop

DecoTengu 0.5.0
---------------
- check if dive is NDL dive before starting dive ascent
- `dt-plot` script reimplemented to use R core plotting functions (ggplot2 no
  longer required)
- added legend to plots created by `dt-plot` script
- added documentation section about comparing dive decompression data with
  `dt-plot` script

DecoTengu 0.4.0
---------------
- trimix support implemented
- travel gas mixes can be added to gas mix list
- added Buhlmann equation description to the documentation

DecoTengu 0.3.0
---------------
- all calculations are performed using pressure instead of depth
- implemented deco model validator to check if first decompression stop is
  at ascent ceiling

DecoTengu 0.2.0
---------------
- gas mix switch is performed in more controlled manner
- API has changed as conveyor functionality is removed from decompression
  engine class; instead, conveyor objects can be used to expand dive
  profile dive steps by replacing Engine.calculate method
- added more detailed Schreiner equation description

DecoTengu 0.1.0
---------------
- initial release

.. vim: sw=4:et:ai
