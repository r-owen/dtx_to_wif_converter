from __future__ import annotations

__all__ = ["DrawdownData", "DrawdownType", "WarpWeftData"]

import dataclasses
import enum
from typing import Any, TypeVar

ValueType = TypeVar("ValueType")


class DrawdownType(enum.Enum):
    SingleTreadle = enum.auto()
    MultiTreadle = enum.auto()
    Liftplan = enum.auto()


@dataclasses.dataclass
class WarpWeftData:
    """Information for the WARP or WEFT sections of a wif

    Parameters:
    * threads: number of threads. DrawdownData increases the value if needed,
      so the default value of 0 results in the minimum required
      to satisfy the drawdown.
    * color: default color index (index into color table)
    * color_rgb: default color as r,g,b
    * spacing: default thread spacing
    * thickness: default thread thickness
    * units: units for spacing and thickness
    """

    threads: int = 0
    color: int | None = None
    color_rgb: tuple[int, int, int] | None = None
    spacing: float | None = None
    thickness: float | None = None
    units: str | None = None


@dataclasses.dataclass
class DrawdownData:
    """Data for a drawdown.

    The contents and format are intended to match the WIF specification.
    Thus indices are 1-based.

    Note that 0 is the standard value for "does not exist".

    Parameters
    ----------
    * name: original file name
    * threading: dict of thread index: shafts
        where shaft is a tuple of 0-based shafts.
        Omitted threads are not threaded on any shaft.
        Also -1 is the standard value for a non-existent shaft.
        Note that is unusual, but supported by WIF, for a thread to be threaded
        on more than one shaft; that is why the values are tuples.
    * tieup: list of treadles, where each treadle is a tuple of shafts.
    * treadling: dict of pick index: treadles, where treadles is a tuple
      of treadles.
    * liftplan: list dict of pick: shafts where shafts is a tuple
      of-based shafts. Omitted picks lift nothing.
    * color_table: dict of color index: color tuple, where each color
      is a tuple of (r, g, b) values. The keys must include all integers
      from 1 through len(color_table).
    * warp: warp data; see WarpWeftData
    * weft: weft data; see WarpWeftData
    * warp_colors: color for each warp thread,
      as a dict of thread index: index into color_table
    * warp_spacing: space each thread takes up,
      as a dict of thread index: spacing
    * warp_thickness: thickness of each thread,
      as a dict of thread index: thickness
    * weft_colors: color for each weft thread,
      as a dict of thread index: index into color_table
    * weft_spacing: space each thread takes up,
      as a dict of thread index: spacing
    * weft_thickness: thickness of each thread,
      as a dict of thread index: thickness
    * color_range: minimum, maximum allowed color value (inclusive)
    * is_rising_shed: if true, shafts go up, if false, shafts go down
    * source_program: name of program that wrote the original file
    * source_version: version of pogram that wrote the original file
    * num_shafts: number of shafts
    * num_treadles: number of treadles

    Notes
    -----
    ``warp.threads``, ``num_shafts``, ``num_treadles``,
    and ``weft.threads`` are increased, if needed, based on computation
    from ``threading``, ``tieup``, ``treadling``, and ``liftplan``.
    Thus you can set each of these to 0 (the default) to have them set to
    the smallest value required.

    Warp/weft colors, spacing, and thickness are post-processed
    to elide default values and put entries in thread order.

    The field names match wif section names, e.g.
    WARP COLORS, WEFT SPACING, WARP THICKNESS.

    Raises
    ------
    RuntimeError
        If there is missing treadling information. The data must
        either include both of tieup and treadling, or else liftplan.
    RuntimeError
        If there are more treadles in treadling than in tieup.
    RuntimeError
        If any color values are out of range.
    RuntimeError
        If the color keys are not a proper sequence 1, 2, ... N.
    RuntimeError
        If ``warp_colors`` or ``weft_colors`` is specified,
        but not ``color_table``.
    RuntimeError
        If ``color_table`` is specified, but not ``color_range``.
    RuntimeError
        If ``color_range`` invalid: length != 2 or
        min (element 0) >= max (element 1)
    RuntimeError
        If there are more treadles in the treadling than in the tieup.
    """

    name: str
    threading: dict[int, tuple[int, ...]]
    tieup: dict[int, tuple[int, ...]]
    treadling: dict[int, tuple[int, ...]]
    liftplan: dict[int, tuple[int, ...]]
    color_table: dict[int, tuple[int, int, int]]
    warp: WarpWeftData
    weft: WarpWeftData
    warp_colors: dict[int, int] = dataclasses.field(default_factory=dict)
    warp_spacing: dict[int, float] = dataclasses.field(default_factory=dict)
    warp_thickness: dict[int, float] = dataclasses.field(default_factory=dict)
    weft_colors: dict[int, int] = dataclasses.field(default_factory=dict)
    weft_spacing: dict[int, float] = dataclasses.field(default_factory=dict)
    weft_thickness: dict[int, float] = dataclasses.field(default_factory=dict)
    color_range: tuple[int, int] | None = None
    is_rising_shed: bool = True
    source_program: str = "?"
    source_version: str = "?"
    num_shafts: int = 0
    num_treadles: int = 0

    def __post_init__(self) -> None:
        # Clean up warp/weft colors, spacing, and threading dicts
        # Put the keys in thread order and elide default values (if known).
        for ww in ("warp", "weft"):
            for field_name in ("colors", "spacing", "thickness"):
                # The default color name has no final s; all other names match
                default_name = {"colors": "color"}.get(field_name, field_name)
                dict_name = f"{ww}_{field_name}"
                default_class = getattr(self, ww, None)
                if default_class is not None:
                    default_value = getattr(default_class, f"{default_name}")
                else:
                    default_value = None
                setattr(
                    self,
                    dict_name,
                    self._clean_dict(getattr(self, dict_name), default_value),
                )

        # Clean up the threading, tieup, treadling, and liftplan dicts
        # by putting keys in order and eliding empty values
        self._clean_dict(self.threading, ())
        self._clean_dict(self.tieup, ())
        self._clean_dict(self.treadling, ())
        self._clean_dict(self.liftplan, ())

        # Clean up the color_table, which has no default values
        self._clean_dict(self.color_table, dataclasses._MISSING_TYPE)

        self.warp.threads = max(len(self.threading), self.warp.threads)

        # Preliminary estimate
        max_shaft_in_threading = max(max(shafts) for shafts in self.threading.values())
        self.num_shafts = max(max_shaft_in_threading, self.num_shafts)

        # Favor tieup + treadling over liftplan
        # since it is easy to convert to liftplan, but not back again
        if self.tieup and self.treadling:
            # There may be shafts in the tieup that were not threaded
            max_shafts_in_liftplan_in_tieup = max(
                len(shafts) for shafts in self.tieup.values()
            )
            self.num_shafts = max(max_shafts_in_liftplan_in_tieup, self.num_shafts)
            self.num_treadles = max(len(self.tieup), self.num_treadles)

            max_num_treadles_per_pick = max(
                len(treadles) for treadles in self.treadling.values()
            )
            if max_num_treadles_per_pick == 1:
                self.drawdown_type = DrawdownType.SingleTreadle
            else:
                self.drawdown_type = DrawdownType.MultiTreadle
            self.weft.threads = max(len(self.treadling), self.weft.threads)

            max_treadle_ind_from_treadling = max(
                max(treadles) for treadles in self.treadling.values()
            )
            if self.num_treadles < max_treadle_ind_from_treadling:
                raise RuntimeError(
                    "Found more treadles in treadling than in tieup: "
                    f"{self.num_treadles} > {max_treadle_ind_from_treadling}"
                )

        elif self.liftplan:
            self.drawdown_type = DrawdownType.Liftplan
            # There may be shafts in the liftplan that were not in the tieup
            max_shafts_in_liftplan = max(
                max(shafts) for shafts in self.liftplan.values()
            )
            self.num_shafts = max(max_shafts_in_liftplan, self.num_shafts)

            self.num_treadles = max(self.num_shafts, self.num_treadles)
            self.weft.threads = max(len(self.liftplan), self.weft.threads)

        else:
            raise RuntimeError(
                "Must specify non-empty liftplan, or both tieup and treadling"
            )

        if self.warp_colors or self.weft_colors:
            if self.color_table is None:
                raise RuntimeError(
                    "warp and/or weft colors specified, but not color table"
                )

        if self.color_table is not None and self.color_range is None:
            raise RuntimeError("color table specified, but not color range")

        if self.color_range is not None:
            if len(self.color_range) != 2:
                raise RuntimeError(
                    f"Invalid color range={self.color_range}; must be two values"
                )

            if self.color_range[0] >= self.color_range[1]:
                raise RuntimeError(
                    f"Invalid color range={self.color_range}; min must be < max"
                )

            if self.color_table:
                if list(self.color_table.keys()) != list(
                    range(1, len(self.color_table) + 1)
                ):
                    raise RuntimeError(
                        f"Color table keys {list(self.color_table.keys())} "
                        f"not 1, 2, ... {len(self.color_table)}"
                    )
                for i, color_rgb in self.color_table.items():
                    if (
                        min(color_rgb) < self.color_range[0]
                        or max(color_rgb) > self.color_range[1]
                    ):
                        raise RuntimeError(
                            f"color table entry {i}={color_rgb} invalid: "
                            f"one or more values not in range "
                            f"[{self.color_range[0]}, {self.color_range[1]}]"
                        )

    def _clean_dict(
        self, data: dict[int, ValueType], default_value: Any
    ) -> dict[int, ValueType]:
        return {key: data[key] for key in sorted(data) if data[key] != default_value}
