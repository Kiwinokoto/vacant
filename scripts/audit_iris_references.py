#!/usr/bin/env python3
"""Audit Paris IRIS identifiers across authenticated Insee source vintages.

Identity of codes does NOT establish identity of geometry. Does not modify
originals, create geometric data, or publish any census microdata.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
from zipfile import ZipFile

REF = {
    2008: ("iris-ref2008", "IRIS_table_geo2008.zip", ".xls"),
    2013: ("iris-ref2013", "IRIS_table_geo2013.zip", ".xls"),
    2018: ("iris-ref2018", "reference_IRIS_geo2018.zip", ".xls"),
    2025: ("iris-ref2025", "reference_IRIS_geo2025.zip", ".xlsx"),
}
CENSUS = {
    2008: ("rp2006", "BTX_IC_LOG_2006.xls", 2006),
    2013: ("rp2011", "infra-logement-2011.zip", 2011),
    2018: ("rp2016", "base-ic-logement-2016.zip", 2016),
}
CROSSWALK = ("iris-passage2013-2008", "IRIS_table_passage_geo2013_geo2008.zip")
PARIS = "751"
COUNT = 992


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(262144), b""):
            h.update(chunk)
    return h.hexdigest()


def audited_file(root, manifest_dir, source, name):
    target = root / source / name
    matches = list(manifest_dir.glob(source + "-*.json"))
    if not target.is_file() or len(matches) != 1:
        raise ValueError(f"Expected one immutable source and manifest: {source}")
    info = json.loads(matches[0].read_text(encoding="utf-8"))
    if (info.get("dataset_id") != source or
        info.get("filename") != str(Path("raw") / "insee" / source / name) or
        not str(info.get("request_url", "")).startswith("https://www.insee.fr/") or
        info.get("sha256") != sha256(target)):
        raise ValueError(f"Provenance or source checksum failure: {source}")
    return target, info


def one_workbook(path, extension):
    import xlrd
    from openpyxl import load_workbook
    if path.suffix.lower() == ".zip":
        with ZipFile(path) as zipfile:
            files = [z for z in zipfile.infolist() if not z.is_dir()]
            if len(files) != 1 or not files[0].filename.lower().endswith(extension):
                raise ValueError(f"Unexpected zipped spreadsheet: {path}")
            if files[0].file_size > 160_000_000:
                raise ValueError("Spreadsheet exceeds audit size limit")
            data = zipfile.read(files[0])
    else:
        if path.suffix.lower() != extension:
            raise ValueError("Unexpected raw workbook format")
        data = path.read_bytes()
    if extension == ".xls":
        workbook = xlrd.open_workbook(file_contents=data, on_demand=True)
        sheet = workbook.sheet_by_index(0)
        return sheet, "xls"
    workbook = load_workbook(io.BytesIO(data), read_only=True, data_only=True)
    sheet = workbook.worksheets[0]
    sheet.reset_dimensions()
    return sheet, "xlsx"


def read_paris(workbook, fmt, expected_geography, strict_reference=False):
    """Select code + label + type only, rejecting duplicates."""
    if fmt == "xls":
        heads = [[str(x) for x in workbook.row_values(i)] for i in range(min(8, workbook.nrows))]
        metadata = " ".join(" ".join(row[:2]) for row in heads[:4])
        header = next((i for i, row in enumerate(heads) if "CODE_IRIS" in row), None)
        if header is None:
            if strict_reference:
                raise ValueError("CODE_IRIS header missing")
            header = next((i for i, row in enumerate(heads) if row[0] == "IRIS"), None)
        if header is None:
            raise ValueError("IRIS column missing")
        cols = heads[header]
        code_index = cols.index("CODE_IRIS") if "CODE_IRIS" in cols else cols.index("IRIS")
        name_index = cols.index("LIB_IRIS") if "LIB_IRIS" in cols else None
        type_index = cols.index("TYP_IRIS") if "TYP_IRIS" in cols else None
        rows = (workbook.row_values(i) for i in range(header + 1, workbook.nrows))
    else:
        iterable = iter(workbook.values)
        heads = [list(next(iterable, [])) for _ in range(8)]
        metadata = " ".join(str(x or "") for row in heads[:4] for x in row[:2])
        header = next((i for i, row in enumerate(heads) if "CODE_IRIS" in row), None)
        if header is None:
            raise ValueError("CODE_IRIS header missing")
        cols = heads[header]
        code_index, name_index, type_index = cols.index("CODE_IRIS"), cols.index("LIB_IRIS"), cols.index("TYP_IRIS")
        rows = iter(heads[header + 1:] + list(iterable))  # historical references are not huge
    if strict_reference and str(expected_geography) not in metadata:
        raise ValueError(f"Wrong geography: expected {expected_geography}")
    selected = {}
    for row in rows:
        if code_index >= len(row):
            continue
        code = str(row[code_index]).strip()
        if not code.startswith(PARIS):
            continue
        if len(code) != 9 or not code.isdigit() or code in selected:
            raise ValueError(f"Invalid or duplicate Paris IRIS code: {code}")
        selected[code] = (
            str(row[name_index]).strip() if name_index is not None else "",
            str(row[type_index]).strip() if type_index is not None else "",
        )
    if len(selected) != COUNT:
        raise ValueError(f"Expected {COUNT} Paris IRIS, obtained {len(selected)}")
    return selected


def compare(a, b):
    old, new = set(a), set(b)
    common = old & new
    return {
        "removed_count": len(old - new),
        "added_count": len(new - old),
        "renamed_count": sum(a[x][0] != b[x][0] for x in common),
        "type_changed_count": sum(a[x][1] != b[x][1] for x in common),
    }


def paris_crosswalk_count(path):
    import xlrd
    sheet, _ = one_workbook(path, ".xls")
    # Only the first (2013 -> 2008) sheet describes actual movements.
    header = sheet.row_values(4)
    for name in ("IRIS_GEO2013", "IRIS_GEO2008"):
        if name not in header:
            raise ValueError("Missing crosswalk code column")
    columns = [header.index(s) for s in ("IRIS_GEO2013", "IRIS_GEO2008")]
    paris_rows = []
    for i in range(5, sheet.nrows):
        values = sheet.row_values(i)
        if any(str(values[j]).startswith(PARIS) for j in columns):
            paris_rows.append(tuple(str(values[j]) for j in columns))
    return len(paris_rows)


def audit(data_root):
    raw = data_root / "raw" / "insee"
    manifests = data_root / "manifests"
    references, evidence = {}, {}
    for geography, (name, filename, extension) in REF.items():
        path, manifest = audited_file(raw, manifests, name, filename)
        wb, fmt = one_workbook(path, extension)
        references[geography] = read_paris(wb, fmt, geography, strict_reference=True)
        evidence[str(geography)] = {
            "url": manifest["request_url"],
            "sha256": manifest["sha256"],
            "paris_iris_count": len(references[geography]),
        }
    census = {}
    for geography, (name, filename, year) in CENSUS.items():
        path, _ = audited_file(raw, manifests, name, filename)
        wb, fmt = one_workbook(path, ".xls")
        census[year] = read_paris(wb, fmt, geography)
        if set(census[year]) != set(references[geography]):
            raise ValueError(f"Census/reference code mismatch: RP{year} versus geography {geography}")
    p, _ = audited_file(raw, manifests, *CROSSWALK)
    passage = paris_crosswalk_count(p)
    return {
        "study_area": "Paris",
        "metric": "official_iris_identifiers_not_geometry",
        "official_references": evidence,
        "census_years_matched": sorted(census),
        "comparisons": {
            f"{a}-{b}": compare(references[a], references[b])
            for a, b in ((2008, 2013), (2013, 2018), (2018, 2025), (2008, 2025))
        },
        "iris_2008_to_2013_crosswalk_rows_paris": passage,
        "geometric_conclusion": "not_verified; matching codes do not prove same polygon",
        "published": False,
    }


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument("--data-root", type=Path, default=Path("/srv/vacant/data"))
    args = cli.parse_args()
    print(json.dumps(audit(args.data_root), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
