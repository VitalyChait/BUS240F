#!/usr/bin/env python3
"""Component 2: Build Vitaly_Chait_Final_Project_Workbook.twbx from starter.

Preserves the starter's exact workbook metadata, manifest, connection,
and object-graph relationship while adding verified calculated fields,
column-instances, 6 structured worksheets, and matching window entries
following strict Tableau 18.1 / 2025.2 XML ordering rules.
"""

from __future__ import annotations

import uuid
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
STARTER_TWBX = REPO_ROOT / "BUS240F_Final_Project_Starter.twbx"
OUTPUT_TWBX = REPO_ROOT / "Vitaly_Chait_Final_Project_Workbook.twbx"
DATA_DIR = REPO_ROOT / "Data"

DS_NAME = "federated.1uzq3s41802ykr10f4fc80617xzf"
DS_CAPTION = "Weekly_Activity+"
USER_NS = "http://www.tableausoftware.com/xml/user"
USER_OP = f"{{{USER_NS}}}op"

CALC_WITHIN_BUDGET = "[Calculation_2911717947329445888]"
CALC_SHARED_10WK = "[Calculation_2911717947329445889]"
CALC_SCHED_RECS = "[Calculation_2911717947329445890]"

AFFORDABLE_OPTIONS = [
    "L01_A", "L02_A", "L02_B", "L03_A", "L03_B", "L04_A", "L06_A", "L06_B"
]


def new_uuid_braced() -> str:
    return "{" + str(uuid.uuid4()).upper() + "}"


def indent_xml(elem: ET.Element, level: int = 0) -> None:
    """Apply clean 2-space indentation to XML elements."""
    ET.indent(elem, space="  ", level=level)


def fq(instance_name: str) -> str:
    return f"[{DS_NAME}].{instance_name}"


def make_col_def(col_meta: dict[str, str]) -> ET.Element:
    attrib = {k: v for k, v in col_meta.items() if k != "formula"}
    el = ET.Element("column", attrib)
    if "formula" in col_meta:
        ET.SubElement(el, "calculation", {"class": "tableau", "formula": col_meta["formula"]})
    return el


def make_ci_def(ci_meta: dict[str, str]) -> ET.Element:
    return ET.Element("column-instance", ci_meta)


def build_measure_names_filter(measure_instances: list[str]) -> ET.Element:
    flt = ET.Element(
        "filter",
        {"class": "categorical", "column": fq("[:Measure Names]")},
    )
    gf = ET.SubElement(flt, "groupfilter", {"function": "union", USER_OP: "manual"})
    for inst in measure_instances:
        ET.SubElement(
            gf,
            "groupfilter",
            {
                "function": "member",
                "level": "[:Measure Names]",
                "member": f'"{fq(inst)}"',
            },
        )
    return flt


def build_categorical_filter(col_inst: str, members: list[str], quote_members: bool = True) -> ET.Element:
    flt = ET.Element(
        "filter",
        {"class": "categorical", "column": fq(col_inst)},
    )
    gf = ET.SubElement(flt, "groupfilter", {"function": "union", USER_OP: "manual"})
    for m in members:
        member_val = f'"{m}"' if quote_members else m
        ET.SubElement(
            gf,
            "groupfilter",
            {
                "function": "member",
                "level": col_inst,
                "member": member_val,
            },
        )
    return flt


def build_worksheet(
    name: str,
    dep_columns: list[dict[str, str]],
    dep_instances: list[dict[str, str]],
    filters: list[ET.Element],
    rows_expr: str | None,
    cols_expr: str | None,
    mark_class: str,
    encodings: list[tuple[str, str]],
    text_formats: list[tuple[str, str]] | None = None,
    header_widths: list[tuple[str, str]] | None = None,
    cell_widths: list[tuple[str, str]] | None = None,
    show_labels: bool = True,
) -> ET.Element:
    ws = ET.Element("worksheet", {"name": name})
    table = ET.SubElement(ws, "table")

    # 1. <view>
    view = ET.SubElement(table, "view")
    dss = ET.SubElement(view, "datasources")
    ET.SubElement(dss, "datasource", {"caption": DS_CAPTION, "name": DS_NAME})

    deps = ET.SubElement(view, "datasource-dependencies", {"datasource": DS_NAME})
    # Rule 2.15: ALL <column> elements before ALL <column-instance> elements
    for col in dep_columns:
        deps.append(make_col_def(col))
    for ci in dep_instances:
        deps.append(make_ci_def(ci))

    filter_cols: list[str] = []
    for flt in filters:
        view.append(flt)
        filter_cols.append(flt.attrib["column"])

    if filter_cols:
        slices = ET.SubElement(view, "slices")
        for col_ref in filter_cols:
            c_el = ET.SubElement(slices, "column")
            c_el.text = col_ref

    ET.SubElement(view, "aggregation", {"value": "true"})

    # 2. <style>
    style = ET.SubElement(table, "style")
    if text_formats or cell_widths:
        sr_cell = ET.SubElement(style, "style-rule", {"element": "cell"})
        for field_ref, fmt in (text_formats or []):
            ET.SubElement(
                sr_cell,
                "format",
                {"attr": "text-format", "field": field_ref, "value": fmt},
            )
        for field_ref, w in (cell_widths or []):
            ET.SubElement(
                sr_cell,
                "format",
                {"attr": "width", "field": field_ref, "value": w},
            )
    if header_widths:
        sr_hdr = ET.SubElement(style, "style-rule", {"element": "header"})
        for field_ref, w in header_widths:
            ET.SubElement(
                sr_hdr,
                "format",
                {"attr": "width", "field": field_ref, "value": w},
            )

    # 3. <panes>
    panes = ET.SubElement(table, "panes")
    pane = ET.SubElement(panes, "pane", {"selection-relaxation-option": "selection-relaxation-allow"})
    pview = ET.SubElement(pane, "view")
    ET.SubElement(pview, "breakdown", {"value": "auto"})
    ET.SubElement(pane, "mark", {"class": mark_class})
    if encodings:
        enc_el = ET.SubElement(pane, "encodings")
        for tag, col_ref in encodings:
            ET.SubElement(enc_el, tag, {"column": col_ref})
    pstyle = ET.SubElement(pane, "style")
    msr = ET.SubElement(pstyle, "style-rule", {"element": "mark"})
    ET.SubElement(msr, "format", {"attr": "mark-labels-show", "value": "true" if show_labels else "false"})
    ET.SubElement(msr, "format", {"attr": "mark-labels-cull", "value": "false"})

    # 4. <rows>, 5. <cols>
    rows_el = ET.SubElement(table, "rows")
    if rows_expr:
        rows_el.text = rows_expr
    cols_el = ET.SubElement(table, "cols")
    if cols_expr:
        cols_el.text = cols_expr

    # <simple-id>
    ET.SubElement(ws, "simple-id", {"uuid": new_uuid_braced()})
    return ws


def build_window(name: str, maximized: bool = False) -> ET.Element:
    attrib = {"class": "worksheet", "name": name}
    if maximized:
        attrib["maximized"] = "true"
    win = ET.Element("window", attrib)
    cards = ET.SubElement(win, "cards")

    left = ET.SubElement(cards, "edge", {"name": "left"})
    strip_l = ET.SubElement(left, "strip", {"size": "160"})
    for ctype in ("pages", "filters", "marks"):
        ET.SubElement(strip_l, "card", {"type": ctype})

    top = ET.SubElement(cards, "edge", {"name": "top"})
    s_col = ET.SubElement(top, "strip", {"size": "2147483647"})
    ET.SubElement(s_col, "card", {"type": "columns"})
    s_row = ET.SubElement(top, "strip", {"size": "2147483647"})
    ET.SubElement(s_row, "card", {"type": "rows"})
    s_ttl = ET.SubElement(top, "strip", {"size": "31"})
    ET.SubElement(s_ttl, "card", {"type": "title"})

    ET.SubElement(win, "simple-id", {"uuid": new_uuid_braced()})
    return win


def build_workbook() -> None:
    ET.register_namespace("user", USER_NS)

    with zipfile.ZipFile(STARTER_TWBX, "r") as zf:
        twb_names = [n for n in zf.namelist() if n.endswith(".twb")]
        if len(twb_names) != 1:
            raise RuntimeError(f"Expected 1 .twb in starter, found {twb_names}")
        starter_twb_bytes = zf.read(twb_names[0])

    root = ET.fromstring(starter_twb_bytes)

    # Base column metadata catalog from starter + new calculated columns
    columns_catalog: dict[str, dict[str, str]] = {}
    ds = root.find("./datasources/datasource")
    if ds is None:
        raise RuntimeError("Missing datasource in starter TWB")

    for col_el in ds.findall("column"):
        cname = col_el.attrib["name"]
        meta = dict(col_el.attrib)
        calc = col_el.find("calculation")
        if calc is not None:
            meta["formula"] = calc.attrib["formula"]
        columns_catalog[cname] = meta

    # Add new calculated columns
    new_calcs = [
        {
            "caption": "Shared 10-Week Affordable Flag",
            "datatype": "string",
            "name": CALC_SHARED_10WK,
            "role": "dimension",
            "type": "nominal",
            "formula": (
                "IF [week_start] != #2026-06-22# AND [week_start] != #2026-06-29# "
                "AND [week_start] != #2026-07-20# AND [week_start] != #2026-08-10# "
                "AND [week_start] != #2026-08-24# AND [week_start] != #2026-09-07# "
                'THEN "Shared 10 Weeks" ELSE "Excluded Missing Week" END'
            ),
        },
        {
            "caption": "Scheduled Weekly Records",
            "datatype": "integer",
            "default-format": "n#,##0;-#,##0",
            "name": CALC_SCHED_RECS,
            "role": "measure",
            "type": "quantitative",
            "formula": "COUNT([week_start])",
        },
    ]
    for nc in new_calcs:
        columns_catalog[nc["name"]] = nc

    # Column instances catalog
    ci_catalog: dict[str, dict[str, str]] = {
        "[none:option_id:nk]": {
            "column": "[option_id]",
            "derivation": "None",
            "name": "[none:option_id:nk]",
            "pivot": "key",
            "type": "nominal",
        },
        "[none:location_name:nk]": {
            "column": "[location_name]",
            "derivation": "None",
            "name": "[none:location_name:nk]",
            "pivot": "key",
            "type": "nominal",
        },
        "[none:window_id:nk]": {
            "column": "[window_id]",
            "derivation": "None",
            "name": "[none:window_id:nk]",
            "pivot": "key",
            "type": "nominal",
        },
        "[none:observation_status:nk]": {
            "column": "[observation_status]",
            "derivation": "None",
            "name": "[none:observation_status:nk]",
            "pivot": "key",
            "type": "nominal",
        },
        "[none:week_start:ok]": {
            "column": "[week_start]",
            "derivation": "None",
            "name": "[none:week_start:ok]",
            "pivot": "key",
            "type": "ordinal",
        },
        "[none:week_start:qk]": {
            "column": "[week_start]",
            "derivation": "None",
            "name": "[none:week_start:qk]",
            "pivot": "key",
            "type": "quantitative",
        },
        f"[none:{CALC_WITHIN_BUDGET.strip('[]')}:nk]": {
            "column": CALC_WITHIN_BUDGET,
            "derivation": "None",
            "name": f"[none:{CALC_WITHIN_BUDGET.strip('[]')}:nk]",
            "pivot": "key",
            "type": "nominal",
        },
        f"[none:{CALC_SHARED_10WK.strip('[]')}:nk]": {
            "column": CALC_SHARED_10WK,
            "derivation": "None",
            "name": f"[none:{CALC_SHARED_10WK.strip('[]')}:nk]",
            "pivot": "key",
            "type": "nominal",
        },
        f"[usr:{CALC_SCHED_RECS.strip('[]')}:qk]": {
            "column": CALC_SCHED_RECS,
            "derivation": "User",
            "name": f"[usr:{CALC_SCHED_RECS.strip('[]')}:qk]",
            "pivot": "key",
            "type": "quantitative",
        },
        "[cnt:observed_passages:qk]": {
            "column": "[observed_passages]",
            "derivation": "Count",
            "name": "[cnt:observed_passages:qk]",
            "pivot": "key",
            "type": "quantitative",
        },
        "[sum:observed_passages:qk]": {
            "column": "[observed_passages]",
            "derivation": "Sum",
            "name": "[sum:observed_passages:qk]",
            "pivot": "key",
            "type": "quantitative",
        },
        "[avg:observed_passages:qk]": {
            "column": "[observed_passages]",
            "derivation": "Avg",
            "name": "[avg:observed_passages:qk]",
            "pivot": "key",
            "type": "quantitative",
        },
        "[med:observed_passages:qk]": {
            "column": "[observed_passages]",
            "derivation": "Median",
            "name": "[med:observed_passages:qk]",
            "pivot": "key",
            "type": "quantitative",
        },
        "[min:total_pilot_cost_usd:qk]": {
            "column": "[total_pilot_cost_usd]",
            "derivation": "Min",
            "name": "[min:total_pilot_cost_usd:qk]",
            "pivot": "key",
            "type": "quantitative",
        },
    }

    CI_WITHIN_BUDGET = f"[none:{CALC_WITHIN_BUDGET.strip('[]')}:nk]"
    CI_SHARED_10WK = f"[none:{CALC_SHARED_10WK.strip('[]')}:nk]"
    CI_SCHED_RECS = f"[usr:{CALC_SCHED_RECS.strip('[]')}:qk]"

    # Rebuild <datasource> preserving strict child ordering:
    # connection, aliases, column(s), column-instance(s), layout, style, semantic-values, object-graph
    conn_el = ds.find("connection")
    aliases_el = ds.find("aliases")
    layout_el = ds.find("layout")
    style_el = ds.find("style")
    sem_el = ds.find("semantic-values")
    og_el = ds.find("object-graph")

    ds_children_new: list[ET.Element] = []
    assert conn_el is not None and aliases_el is not None and layout_el is not None
    assert style_el is not None and sem_el is not None and og_el is not None

    ds_children_new.append(conn_el)
    ds_children_new.append(aliases_el)
    for cname in sorted(columns_catalog.keys()):
        ds_children_new.append(make_col_def(columns_catalog[cname]))
    for ciname in sorted(ci_catalog.keys()):
        ds_children_new.append(make_ci_def(ci_catalog[ciname]))
    ds_children_new.append(layout_el)
    ds_children_new.append(style_el)
    ds_children_new.append(sem_el)
    ds_children_new.append(og_el)

    for child in list(ds):
        ds.remove(child)
    for child in ds_children_new:
        ds.append(child)

    def deps_for(col_names: list[str], ci_names: list[str]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
        cols = [columns_catalog[c] for c in sorted(set(col_names))]
        cis = [ci_catalog[ci] for ci in sorted(set(ci_names))]
        return cols, cis

    # 1. Worksheet: 01 Verify the Model
    ws1_cols, ws1_cis = deps_for(
        ["[observation_status]", "[observed_passages]", "[week_start]", CALC_SCHED_RECS],
        ["[none:observation_status:nk]", CI_SCHED_RECS, "[cnt:observed_passages:qk]", "[sum:observed_passages:qk]"],
    )
    ws1 = build_worksheet(
        name="01 Verify the Model",
        dep_columns=ws1_cols,
        dep_instances=ws1_cis,
        filters=[
            build_measure_names_filter(
                [CI_SCHED_RECS, "[cnt:observed_passages:qk]", "[sum:observed_passages:qk]"]
            )
        ],
        rows_expr=fq("[none:observation_status:nk]"),
        cols_expr=fq("[:Measure Names]"),
        mark_class="Text",
        encodings=[("text", fq("[Multiple Values]"))],
        text_formats=[
            (fq(CI_SCHED_RECS), "n#,##0;-#,##0"),
            (fq("[cnt:observed_passages:qk]"), "n#,##0;-#,##0"),
            (fq("[sum:observed_passages:qk]"), "n#,##0;-#,##0"),
        ],
        cell_widths=[(fq("[:Measure Names]"), "180")],
        header_widths=[(fq("[none:observation_status:nk]"), "140")],
    )

    # 2. Worksheet: 01b Option Cost & Completeness Audit
    ws1b_cols, ws1b_cis = deps_for(
        [
            CALC_WITHIN_BUDGET, "[total_pilot_cost_usd]", "[option_id]",
            "[location_name]", "[window_id]", "[observed_passages]",
            "[week_start]", CALC_SCHED_RECS,
        ],
        [
            CI_WITHIN_BUDGET, "[none:option_id:nk]", "[none:location_name:nk]",
            "[none:window_id:nk]", "[min:total_pilot_cost_usd:qk]",
            "[cnt:observed_passages:qk]", CI_SCHED_RECS,
        ],
    )
    ws1b = build_worksheet(
        name="01b Option Cost & Completeness Audit",
        dep_columns=ws1b_cols,
        dep_instances=ws1b_cis,
        filters=[
            build_measure_names_filter(
                ["[min:total_pilot_cost_usd:qk]", "[cnt:observed_passages:qk]", CI_SCHED_RECS]
            )
        ],
        rows_expr=(
            f"({fq(CI_WITHIN_BUDGET)} / ({fq('[none:option_id:nk]')} / "
            f"({fq('[none:location_name:nk]')} / {fq('[none:window_id:nk]')})))"
        ),
        cols_expr=fq("[:Measure Names]"),
        mark_class="Text",
        encodings=[("text", fq("[Multiple Values]"))],
        text_formats=[
            (fq("[min:total_pilot_cost_usd:qk]"), 'c"$"#,##0;("$"#,##0)'),
            (fq("[cnt:observed_passages:qk]"), "n#,##0;-#,##0"),
            (fq(CI_SCHED_RECS), "n#,##0;-#,##0"),
        ],
        cell_widths=[(fq("[:Measure Names]"), "170")],
    )

    # 3. Worksheet: 01c Representative Source Check (L01_A)
    ws1c_cols, ws1c_cis = deps_for(
        ["[option_id]", "[week_start]", "[observation_status]", "[observed_passages]", CALC_SCHED_RECS],
        ["[none:option_id:nk]", "[none:week_start:ok]", "[none:observation_status:nk]", CI_SCHED_RECS, "[sum:observed_passages:qk]"],
    )
    ws1c = build_worksheet(
        name="01c Representative Source Check (L01_A)",
        dep_columns=ws1c_cols,
        dep_instances=ws1c_cis,
        filters=[
            build_categorical_filter("[none:option_id:nk]", ["L01_A"], quote_members=True),
            build_categorical_filter("[none:week_start:ok]", ["#2026-06-08#", "#2026-06-29#"], quote_members=False),
            build_measure_names_filter([CI_SCHED_RECS, "[sum:observed_passages:qk]"]),
        ],
        rows_expr=(
            f"({fq('[none:option_id:nk]')} / ({fq('[none:week_start:ok]')} / "
            f"{fq('[none:observation_status:nk]')}))"
        ),
        cols_expr=fq("[:Measure Names]"),
        mark_class="Text",
        encodings=[("text", fq("[Multiple Values]"))],
        text_formats=[
            (fq(CI_SCHED_RECS), "n#,##0;-#,##0"),
            (fq("[sum:observed_passages:qk]"), "n#,##0;-#,##0"),
        ],
        cell_widths=[(fq("[:Measure Names]"), "180")],
    )

    # 4. Worksheet: 02 Build the Decision
    ws2_cols, ws2_cis = deps_for(
        [
            CALC_WITHIN_BUDGET, "[total_pilot_cost_usd]", "[option_id]",
            "[location_name]", "[window_id]", "[observed_passages]",
        ],
        [
            CI_WITHIN_BUDGET, "[none:option_id:nk]", "[none:location_name:nk]",
            "[none:window_id:nk]", "[avg:observed_passages:qk]", "[med:observed_passages:qk]",
            "[min:total_pilot_cost_usd:qk]", "[cnt:observed_passages:qk]",
        ],
    )
    ws2 = build_worksheet(
        name="02 Build the Decision",
        dep_columns=ws2_cols,
        dep_instances=ws2_cis,
        filters=[
            build_measure_names_filter(["[avg:observed_passages:qk]", "[med:observed_passages:qk]"])
        ],
        rows_expr=(
            f"({fq(CI_WITHIN_BUDGET)} / ({fq('[none:option_id:nk]')} / "
            f"({fq('[none:location_name:nk]')} / {fq('[none:window_id:nk]')})))"
        ),
        cols_expr=f"({fq('[:Measure Names]')} * {fq('[Multiple Values]')})",
        mark_class="Bar",
        encodings=[
            ("color", fq(CI_WITHIN_BUDGET)),
            ("text", fq("[Multiple Values]")),
            ("lod", fq("[min:total_pilot_cost_usd:qk]")),
            ("lod", fq("[cnt:observed_passages:qk]")),
        ],
        text_formats=[
            (fq("[avg:observed_passages:qk]"), "n#,##0.0;-#,##0.0"),
            (fq("[med:observed_passages:qk]"), "n#,##0.0;-#,##0.0"),
            (fq("[min:total_pilot_cost_usd:qk]"), 'c"$"#,##0;("$"#,##0)'),
            (fq("[cnt:observed_passages:qk]"), "n#,##0;-#,##0"),
        ],
    )

    # 5. Worksheet: 03 Weekly Trajectory & Outliers
    ws3_cols, ws3_cis = deps_for(
        [
            CALC_WITHIN_BUDGET, "[total_pilot_cost_usd]", "[option_id]",
            "[location_name]", "[window_id]", "[week_start]", "[observed_passages]",
        ],
        [
            CI_WITHIN_BUDGET, "[none:option_id:nk]", "[none:location_name:nk]",
            "[none:window_id:nk]", "[none:week_start:qk]", "[avg:observed_passages:qk]",
            "[min:total_pilot_cost_usd:qk]",
        ],
    )
    ws3 = build_worksheet(
        name="03 Weekly Trajectory & Outliers",
        dep_columns=ws3_cols,
        dep_instances=ws3_cis,
        filters=[],
        rows_expr=f"({fq(CI_WITHIN_BUDGET)} * {fq('[avg:observed_passages:qk]')})",
        cols_expr=fq("[none:week_start:qk]"),
        mark_class="Line",
        encodings=[
            ("color", fq("[none:option_id:nk]")),
            ("lod", fq("[none:location_name:nk]")),
            ("lod", fq("[none:window_id:nk]")),
            ("lod", fq("[min:total_pilot_cost_usd:qk]")),
        ],
        text_formats=[
            (fq("[avg:observed_passages:qk]"), "n#,##0;-#,##0"),
            (fq("[min:total_pilot_cost_usd:qk]"), 'c"$"#,##0;("$"#,##0)'),
        ],
        show_labels=False,
    )

    # 6. Worksheet: 04 Shared-Week Sensitivity Test
    ws4_cols, ws4_cis = deps_for(
        [
            CALC_SHARED_10WK, "[week_start]", "[option_id]", "[location_name]",
            "[window_id]", "[total_pilot_cost_usd]", "[observed_passages]",
        ],
        [
            CI_SHARED_10WK, "[none:option_id:nk]", "[none:location_name:nk]",
            "[none:window_id:nk]", "[avg:observed_passages:qk]", "[med:observed_passages:qk]",
            "[min:total_pilot_cost_usd:qk]", "[cnt:observed_passages:qk]",
        ],
    )
    ws4 = build_worksheet(
        name="04 Shared-Week Sensitivity Test",
        dep_columns=ws4_cols,
        dep_instances=ws4_cis,
        filters=[
            build_categorical_filter(CI_SHARED_10WK, ["Shared 10 Weeks"], quote_members=True),
            build_categorical_filter("[none:option_id:nk]", AFFORDABLE_OPTIONS, quote_members=True),
            build_measure_names_filter(["[avg:observed_passages:qk]", "[med:observed_passages:qk]"]),
        ],
        rows_expr=(
            f"({fq('[none:option_id:nk]')} / ({fq('[none:location_name:nk]')} / "
            f"{fq('[none:window_id:nk]')}))"
        ),
        cols_expr=f"({fq('[:Measure Names]')} * {fq('[Multiple Values]')})",
        mark_class="Bar",
        encodings=[
            ("color", fq("[none:option_id:nk]")),
            ("text", fq("[Multiple Values]")),
            ("lod", fq("[min:total_pilot_cost_usd:qk]")),
            ("lod", fq("[cnt:observed_passages:qk]")),
        ],
        text_formats=[
            (fq("[avg:observed_passages:qk]"), "n#,##0.0;-#,##0.0"),
            (fq("[med:observed_passages:qk]"), "n#,##0.0;-#,##0.0"),
            (fq("[min:total_pilot_cost_usd:qk]"), 'c"$"#,##0;("$"#,##0)'),
            (fq("[cnt:observed_passages:qk]"), "n#,##0;-#,##0"),
        ],
    )

    worksheets = [ws1, ws1b, ws1c, ws2, ws3, ws4]
    ws_parent = root.find("worksheets")
    assert ws_parent is not None
    for child in list(ws_parent):
        ws_parent.remove(child)
    for ws in worksheets:
        ws_parent.append(ws)

    win_parent = root.find("windows")
    assert win_parent is not None
    for child in list(win_parent):
        win_parent.remove(child)
    for idx, ws in enumerate(worksheets):
        win_parent.append(build_window(ws.attrib["name"], maximized=(idx == 0)))

    indent_xml(root)

    xml_body = ET.tostring(root, encoding="unicode")
    # Ensure XML declaration and starter build comment + xmlns:user retention
    if 'xmlns:user="http://www.tableausoftware.com/xml/user"' not in xml_body and "xmlns:user='http://www.tableausoftware.com/xml/user'" not in xml_body:
        xml_body = xml_body.replace(
            "<workbook ",
            '<workbook xmlns:user="http://www.tableausoftware.com/xml/user" ',
            1,
        )

    final_twb = (
        "<?xml version='1.0' encoding='utf-8' ?>\n\n"
        "<!-- build 20252.25.0710.1712                               -->\n"
        + xml_body
        + "\n"
    )

    co_bytes = (DATA_DIR / "Candidate_Options.csv").read_bytes()
    wa_bytes = (DATA_DIR / "Weekly_Activity.csv").read_bytes()

    with zipfile.ZipFile(OUTPUT_TWBX, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("Vitaly_Chait_Final_Project_Workbook.twb", final_twb.encode("utf-8"))
        zf.writestr("Data/Prototype/Candidate_Options.csv", co_bytes)
        zf.writestr("Data/Prototype/Weekly_Activity.csv", wa_bytes)

    print(f"Successfully generated {OUTPUT_TWBX.name} with {len(worksheets)} worksheets.")


if __name__ == "__main__":
    build_workbook()
