#!/usr/bin/env python3
"""Component 2: 18-Point Automated Validation for Vitaly_Chait_Final_Project_Workbook.twbx."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TWBX_PATH = REPO_ROOT / "Vitaly_Chait_Final_Project_Workbook.twbx"
DATA_DIR = REPO_ROOT / "Data"

DS_NAME = "federated.1uzq3s41802ykr10f4fc80617xzf"
VIRTUAL_INSTANCES = {"[:Measure Names]", "[Multiple Values]"}
UUID_RE = re.compile(r"^\{[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}\}$")
FED_TOKEN_RE = re.compile(r"\[([^\]]+)\]\.\[([^\]]+)\]")


def validate_twbx() -> int:
    results: list[tuple[str, bool, str]] = []

    def record(cid: str, passed: bool, msg: str) -> None:
        results.append((cid, passed, msg))

    # Check 2.1: Valid ZIP archive containing .twb and both CSVs
    if not TWBX_PATH.exists():
        record("Check 2.1", False, f"{TWBX_PATH.name} does not exist")
        for cid, ok, msg in results:
            print(f"[{'PASS' if ok else 'FAIL'}] {cid}: {msg}")
        return 1

    with zipfile.ZipFile(TWBX_PATH, "r") as zf:
        bad = zf.testzip()
        names = zf.namelist()
        twb_files = [n for n in names if n.endswith(".twb")]
        has_co = "Data/Prototype/Candidate_Options.csv" in names
        has_wa = "Data/Prototype/Weekly_Activity.csv" in names
        c21 = bad is None and len(twb_files) == 1 and has_co and has_wa
        record("Check 2.1", c21, f"bad_zip={bad}, twb={twb_files}, has_co={has_co}, has_wa={has_wa}")

        # Check 2.2: Embedded CSVs match Data/*.csv byte-for-byte
        emb_co = zf.read("Data/Prototype/Candidate_Options.csv") if has_co else b""
        emb_wa = zf.read("Data/Prototype/Weekly_Activity.csv") if has_wa else b""
        disk_co = (DATA_DIR / "Candidate_Options.csv").read_bytes()
        disk_wa = (DATA_DIR / "Weekly_Activity.csv").read_bytes()
        c22 = emb_co == disk_co and emb_wa == disk_wa
        record("Check 2.2", c22, f"co_match={emb_co == disk_co}, wa_match={emb_wa == disk_wa}")

        twb_bytes = zf.read(twb_files[0]) if twb_files else b""

    twb_text = twb_bytes.decode("utf-8", errors="replace")

    # Check 2.3: Parse XML & retain xmlns:user and root attrs
    parse_err = None
    root = None
    try:
        root = ET.fromstring(twb_bytes)
    except ET.ParseError as exc:
        parse_err = str(exc)

    has_xmlns_user = (
        "xmlns:user='http://www.tableausoftware.com/xml/user'" in twb_text
        or 'xmlns:user="http://www.tableausoftware.com/xml/user"' in twb_text
    )
    attrs_ok = (
        root is not None
        and root.tag == "workbook"
        and root.attrib.get("original-version") == "18.1"
        and root.attrib.get("version") == "18.1"
        and root.attrib.get("source-platform") == "mac"
        and "source-build" in root.attrib
    )
    c23 = parse_err is None and has_xmlns_user and attrs_ok
    record("Check 2.3", c23, f"parse_err={parse_err}, xmlns_user={has_xmlns_user}, attrs_ok={attrs_ok}")

    if root is None:
        for cid, ok, msg in results:
            print(f"[{'PASS' if ok else 'FAIL'}] {cid}: {msg}")
        return 1

    # Check 2.4: Root <workbook> children exact order
    expected_root_order = [
        "document-format-change-manifest",
        "preferences",
        "datasources",
        "worksheets",
        "windows",
        "thumbnails",
    ]
    actual_root_order = [child.tag for child in list(root)]
    c24 = actual_root_order == expected_root_order
    record("Check 2.4", c24, f"order={actual_root_order}")

    # Check 2.5: Manifest capability tags
    expected_manifest = {
        "AnimationOnByDefault",
        "MarkAnimation",
        "ObjectModelEncapsulateLegacy",
        "ObjectModelTableType",
        "SchemaViewerObjectModel",
        "SheetIdentifierTracking",
        "WindowsPersistSimpleIdentifiers",
    }
    manifest = root.find("document-format-change-manifest")
    actual_manifest = {c.tag for c in list(manifest)} if manifest is not None else set()
    c25 = expected_manifest.issubset(actual_manifest) and len(actual_manifest) == 7
    record("Check 2.5", c25, f"tags={sorted(actual_manifest)}")

    # Check 2.6: <datasource> children exact XSD order
    ds = root.find("./datasources/datasource")
    ds_tags = [c.tag for c in list(ds)] if ds is not None else []
    # Expected sequence: connection, aliases, column+, column-instance*, layout, style, semantic-values, object-graph
    c26 = False
    if ds is not None and len(ds_tags) >= 7:
        idx = 0
        if ds_tags[0] == "connection" and ds_tags[1] == "aliases":
            idx = 2
            while idx < len(ds_tags) and ds_tags[idx] == "column":
                idx += 1
            col_count = idx - 2
            while idx < len(ds_tags) and ds_tags[idx] == "column-instance":
                idx += 1
            c26 = col_count > 0 and ds_tags[idx:] == ["layout", "style", "semantic-values", "object-graph"]
    record("Check 2.6", c26, f"datasource tag count={len(ds_tags)}")

    # Check 2.7: <object-graph> objects and exact relationship on option_id
    og = ds.find("object-graph") if ds is not None else None
    objs = og.findall("./objects/object") if og is not None else []
    obj_captions = {o.attrib.get("caption") for o in objs}
    rels = og.findall("./relationships/relationship") if og is not None else []
    rel_ok = False
    if len(rels) == 1:
        expr = rels[0].find("expression")
        ops = [e.attrib.get("op") for e in expr.findall("expression")] if expr is not None else []
        ep1 = rels[0].find("first-end-point")
        ep2 = rels[0].find("second-end-point")
        rel_ok = (
            expr is not None
            and expr.attrib.get("op") == "="
            and ops == ["[option_id (Candidate_Options.csv)]", "[option_id]"]
            and ep1 is not None
            and ep2 is not None
        )
    c27 = obj_captions == {"Candidate_Options.csv", "Weekly_Activity.csv"} and rel_ok
    record("Check 2.7", c27, f"objects={sorted(str(x) for x in obj_captions)}, rel_ok={rel_ok}")

    # Check 2.8: Calculated <column> definitions
    ds_cols = ds.findall("column") if ds is not None else []
    ds_col_names = {c.attrib["name"] for c in ds_cols}
    calc_cols = [c for c in ds_cols if c.find("calculation") is not None]
    calc_names = [c.attrib["name"] for c in calc_cols]
    calc_ok = (
        len(calc_cols) >= 2
        and len(calc_names) == len(set(calc_names))
        and all(n.startswith("[Calculation_") and n.endswith("]") for n in calc_names)
        and all(
            c.find("calculation").attrib.get("class") == "tableau"
            and bool(c.find("calculation").attrib.get("formula", "").strip())
            for c in calc_cols
        )
    )
    record("Check 2.8", calc_ok, f"calc_count={len(calc_cols)}, names={calc_names}")

    # Worksheet checks 2.9 - 2.16
    worksheets = root.findall("./worksheets/worksheet")
    c29_ok = True
    c210_ok = True
    c211_ok = True
    c212_ok = True
    c213_ok = True
    c214_ok = True
    c215_ok = True
    c216_ok = True
    errors: list[str] = []

    for ws in worksheets:
        wname = ws.attrib.get("name", "<unnamed>")
        ws_children = [c.tag for c in list(ws)]
        if ws_children != ["table", "simple-id"]:
            c29_ok = False
            errors.append(f"2.9 {wname}: {ws_children}")
            continue

        table = ws.find("table")
        assert table is not None
        t_children = [c.tag for c in list(table)]
        if t_children != ["view", "style", "panes", "rows", "cols"]:
            c210_ok = False
            errors.append(f"2.10 {wname}: {t_children}")

        view = table.find("view")
        assert view is not None
        v_tags = [c.tag for c in list(view)]

        # Check 2.11: datasources, datasource-dependencies?, filter*, slices(iff filters>0), aggregation
        idx = 0
        v_valid = False
        if idx < len(v_tags) and v_tags[idx] == "datasources":
            idx += 1
            if idx < len(v_tags) and v_tags[idx] == "datasource-dependencies":
                deps_el = list(view)[idx]
                if len(list(deps_el)) == 0:
                    errors.append(f"2.11 {wname}: empty datasource-dependencies")
                else:
                    idx += 1
            flt_count = 0
            while idx < len(v_tags) and v_tags[idx] == "filter":
                flt_count += 1
                idx += 1
            if flt_count > 0:
                if idx < len(v_tags) and v_tags[idx] == "slices":
                    idx += 1
                else:
                    errors.append(f"2.11 {wname}: missing <slices> after {flt_count} filters")
            if idx == len(v_tags) - 1 and v_tags[idx] == "aggregation":
                agg_el = list(view)[idx]
                if agg_el.attrib.get("value") == "true" and (flt_count == 0 or "slices" in v_tags):
                    v_valid = True
        if not v_valid:
            c211_ok = False
            errors.append(f"2.11 {wname}: {v_tags}")

        # Check 2.12: filter column == slices column parity
        flt_cols = [f.attrib.get("column") for f in view.findall("filter")]
        slices_el = view.find("slices")
        slice_cols = [c.text for c in slices_el.findall("column")] if slices_el is not None else []
        if flt_cols != slice_cols or set(flt_cols) != set(slice_cols):
            c212_ok = False
            errors.append(f"2.12 {wname}: filters={flt_cols} vs slices={slice_cols}")

        # Inspect datasource-dependencies
        deps = view.find("datasource-dependencies")
        dep_cols = deps.findall("column") if deps is not None else []
        dep_cis = deps.findall("column-instance") if deps is not None else []

        # Check 2.15: All <column> before <column-instance>
        if deps is not None:
            seen_ci = False
            for child in list(deps):
                if child.tag == "column-instance":
                    seen_ci = True
                elif child.tag == "column" and seen_ci:
                    c215_ok = False
                    errors.append(f"2.15 {wname}: <column> after <column-instance>")
                elif child.tag not in ("column", "column-instance"):
                    c215_ok = False
                    errors.append(f"2.15 {wname}: unexpected tag {child.tag}")

        dep_col_names = {c.attrib["name"] for c in dep_cols}
        dep_ci_names = {ci.attrib["name"] for ci in dep_cis}

        # Check 2.14: every column-instance column in dep_cols AND main ds
        for ci in dep_cis:
            base = ci.attrib.get("column", "")
            if base not in dep_col_names or base not in ds_col_names:
                c214_ok = False
                errors.append(f"2.14 {wname}: base {base} missing in deps or ds")
        # Also verify base columns referenced by calculated columns in deps
        for dc in dep_cols:
            calc = dc.find("calculation")
            if calc is not None:
                formula = calc.attrib.get("formula", "")
                for ref in re.findall(r"\[[a-zA-Z0-9_]+\]", formula):
                    if ref not in dep_col_names or ref not in ds_col_names:
                        c214_ok = False
                        errors.append(f"2.14 {wname}: formula ref {ref} missing in deps or ds")

        # Check 2.13: every [federated...].[instance] used in rows, cols, encodings, filter, slices
        tokens_to_check: list[str] = []
        for shelf_tag in ("rows", "cols"):
            el = table.find(shelf_tag)
            if el is not None and el.text:
                for ds_tok, inst in FED_TOKEN_RE.findall(el.text):
                    if ds_tok == DS_NAME:
                        tokens_to_check.append(f"[{inst}]")
        for pane in table.findall("./panes/pane"):
            enc = pane.find("encodings")
            if enc is not None:
                for child in list(enc):
                    col_attr = child.attrib.get("column", "")
                    for ds_tok, inst in FED_TOKEN_RE.findall(col_attr):
                        if ds_tok == DS_NAME:
                            tokens_to_check.append(f"[{inst}]")
        for flt in view.findall("filter"):
            for ds_tok, inst in FED_TOKEN_RE.findall(flt.attrib.get("column", "")):
                if ds_tok == DS_NAME:
                    tokens_to_check.append(f"[{inst}]")
            for gf in flt.findall(".//groupfilter"):
                m_attr = gf.attrib.get("member", "")
                for ds_tok, inst in FED_TOKEN_RE.findall(m_attr):
                    if ds_tok == DS_NAME:
                        tokens_to_check.append(f"[{inst}]")
        if slices_el is not None:
            for sc in slices_el.findall("column"):
                if sc.text:
                    for ds_tok, inst in FED_TOKEN_RE.findall(sc.text):
                        if ds_tok == DS_NAME:
                            tokens_to_check.append(f"[{inst}]")

        for inst in tokens_to_check:
            if inst in VIRTUAL_INSTANCES:
                continue
            if inst not in dep_ci_names:
                c213_ok = False
                errors.append(f"2.13 {wname}: {inst} missing from datasource-dependencies")

        # Check 2.16: every <pane> has <view><breakdown value='auto'/></view> and <mark .../> before <encodings>
        for pane in table.findall("./panes/pane"):
            p_children = list(pane)
            p_tags = [c.tag for c in p_children]
            has_view_bd = (
                len(p_tags) >= 2
                and p_tags[0] == "view"
                and p_children[0].find("breakdown") is not None
                and p_children[0].find("breakdown").attrib.get("value") == "auto"
                and p_tags[1] == "mark"
                and bool(p_children[1].attrib.get("class"))
            )
            enc_idx = p_tags.index("encodings") if "encodings" in p_tags else None
            order_ok = has_view_bd and (enc_idx is None or enc_idx > 1)
            if not order_ok:
                c216_ok = False
                errors.append(f"2.16 {wname}: pane tags={p_tags}")

    record("Check 2.9", c29_ok, f"checked {len(worksheets)} worksheets")
    record("Check 2.10", c210_ok, "table child sequence valid" if c210_ok else "; ".join(errors))
    record("Check 2.11", c211_ok, "view child sequence valid" if c211_ok else "; ".join(errors))
    record("Check 2.12", c212_ok, "filter/slices exact parity" if c212_ok else "; ".join(errors))
    record("Check 2.13", c213_ok, "all shelf/encoding/filter instances declared" if c213_ok else "; ".join(errors))
    record("Check 2.14", c214_ok, "all base columns declared in deps & datasource" if c214_ok else "; ".join(errors))
    record("Check 2.15", c215_ok, "all <column> before <column-instance> in deps" if c215_ok else "; ".join(errors))
    record("Check 2.16", c216_ok, "pane view/breakdown/mark order valid" if c216_ok else "; ".join(errors))

    # Check 2.17: <worksheets> and <windows> 1-to-1 match, exactly one maximized='true'
    ws_names = [ws.attrib.get("name") for ws in worksheets]
    windows = root.findall("./windows/window")
    win_names = [w.attrib.get("name") for w in windows]
    max_wins = [w.attrib.get("name") for w in windows if w.attrib.get("maximized") == "true"]
    c217 = (
        len(ws_names) == 6
        and ws_names == win_names
        and len(set(ws_names)) == len(ws_names)
        and len(max_wins) == 1
    )
    record("Check 2.17", c217, f"count={len(ws_names)}, maximized={max_wins}")

    # Check 2.18: All <simple-id uuid='{...}' /> valid uppercase UUIDs with zero duplicates
    sids = [el.attrib.get("uuid", "") for el in root.findall(".//simple-id")]
    all_valid_uuid = all(bool(UUID_RE.match(u)) for u in sids)
    c218 = len(sids) == 12 and all_valid_uuid and len(set(sids)) == len(sids)
    record("Check 2.18", c218, f"simple_ids={len(sids)}, unique={len(set(sids))}, valid_fmt={all_valid_uuid}")

    failed = False
    for cid, ok, msg in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {cid}: {msg}")
        if not ok:
            failed = True

    if errors:
        print("\nDetailed diagnostics:")
        for e in errors:
            print("  -", e)

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(validate_twbx())
