#!/usr/bin/env python3
"""Package the audited APUR grid as a reproducible public ODbL derivative.

Only selected public fields already present in the 500 m grid are included.
The original private acquisition ZIP and unused attributes remain private.
"""
from __future__ import annotations

from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import stat
import zipfile

SOURCE_ZIP_SHA = "f6d612844829dbf610fabf89dd442f6c50b4d8b04b33745e55e3e983c6e74e11"
PRIVATE_MANIFEST_SHA = "bb02fe9ac9ef7919018118659e12ac533b098234250eba540c6975e7b273bb0c"
PUBLIC_DATASET_NAME = "apur-paris-grid-500m-2026-10-16-odbl.zip"
LICENCE_URI = "https://opendatacommons.org/licenses/odbl/1-0/"
SOURCE_URI = "https://opendata.apur.org/datasets/emprise-batie-paris"
NOTICE = """# VACANT — emprises bâties de Paris (Apur)

Données d'origine : © Atelier parisien d'urbanisme (Apur).
Source : https://opendata.apur.org/datasets/emprise-batie-paris
Licence de la base d'origine ET de cette base adaptée : ODbL 1.0
Texte de la licence : https://opendatacommons.org/licenses/odbl/1-0/

Archive source téléchargée le 16 octobre 2026, SHA-256 :
f6d612844829dbf610fabf89dd442f6c50b4d8b04b33745e55e3e983c6e74e11
Le millésime scientifique réel de chaque emprise n'est pas attesté.

Transformation reproductible : scripts/build_apur_private_grid.py,
disponible sous https://github.com/Kiwinokoto/vacant.
- Emprises actuelles, converties EPSG:2154 vers EPSG:4326.
- 128 206 enregistrements source ; 104 géométries GEOS invalides et
  13 identifiants métier absents exclus.
- 128 089 emprises uniques ; 456 cellules de 500 m en Lambert-93 ;
  138 381 occurrences, à dédoublonner par object_id.
- Attributs dérivés : object_id, period_code (catégorie de datation
  attribuée à l'emprise), height_m (hauteur médiane h_med en mètres).
- Un polygone qui chevauche plusieurs cellules y apparaît intégralement ;
  ni découpage ni simplification. Les formes invalides ne sont pas réparées.

Cette base ne contient AUCUNE information sur les logements vacants
individuels. Périodes attribuées ne signifient pas existence historique
attestée du bâtiment à une date précise.

Les cellules GeoJSON, le manifeste contenant chaque SHA-256 et cette
notice sont fournis en téléchargement sans restriction technique.
Réutilisation et redistribution sous ODbL 1.0 avec attribution et
respect des droits éventuels sur les contenus tiers.
"""
def sha_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()

def package_grid(source: Path, destination: Path):
    """Write inside a NEW EMPTY staging directory, never touch the input."""
    source, destination = map(Path, (source, destination))
    if not source.is_dir() or not destination.is_dir() or list(destination.iterdir()):
        raise ValueError("Require existing audited source and empty staging destination")
    if destination.is_symlink() or source.is_symlink() or destination.resolve() == source.resolve():
        raise ValueError("Disallow symlink or in-place packaging")
    private_file = source / "manifest.json"
    if private_file.is_symlink() or sha_bytes(private_file.read_bytes()) != PRIVATE_MANIFEST_SHA:
        raise ValueError("Original Apur grid manifest SHA-256 mismatch")
    original = json.loads(private_file.read_text(encoding="utf-8"))
    if (original.get("source_archive_sha256") != SOURCE_ZIP_SHA or
            original.get("license") != "ODbL-1.0" or
            original.get("research_only") is not True or
            original.get("public_release_allowed") is not False or
            original.get("contains_vacancy_data") is not False or
            original.get("scientific_vintage") != "not confirmed by Apur" or
            original.get("cell_count") != 456 or
            original.get("unique_features") != 128089 or
            original.get("source_count") != 128206 or
            original.get("placements") != 138381 or
            original.get("skipped_by_exclusive_reason") !=
                {"invalid_geometry": 104, "missing_business_id": 13}):
        raise ValueError("Source dataset provenance/counts changed")
    cells = original.get("cells")
    if not isinstance(cells, dict) or len(cells) != 456:
        raise ValueError("Incomplete audited 500 m grid")
    expected_names = {m["file"] for m in cells.values()}
    if len(expected_names) != 456:
        raise ValueError("Duplicated cell filename in manifest")
    files = {p.name for p in source.iterdir()}
    if files != expected_names | {"manifest.json"}:
        raise ValueError("Unexpected input file (could reveal private information)")
    for meta in cells.values():
        if (not isinstance(meta, dict) or
                not isinstance(meta.get("file"), str) or
                not meta["file"].startswith("cell_") or
                not meta["file"].endswith(".geojson") or
                "/" in meta["file"] or "\\" in meta["file"]):
            raise ValueError("Unsafe cell filename")
        path = source / meta["file"]
        if not path.is_file() or path.is_symlink() or path.stat().st_size != meta["bytes"]:
            raise ValueError("Missing, linked or size-mismatched cell")
        if sha_bytes(path.read_bytes()) != meta["sha256"]:
            raise ValueError("Cell SHA mismatch: " + meta["file"])
    public = dict(original)
    public["research_only"] = False
    public["public_release_allowed"] = True
    public["license_uri"] = LICENCE_URI
    public["source_uri"] = SOURCE_URI
    public["source_attribution"] = "© Atelier parisien d'urbanisme (Apur)"
    public["public_release_date"] = "2026-10-17"
    public["caution"] = ("Current building footprints, not proof of historical occupation "
                         "or individual residential vacancy. Scientific vintage unknown.")
    manifest = (json.dumps(public, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    written = []
    # Copy only files audited above. No raw Apur data or unknown source attributes.
    for filename in sorted(expected_names):
        target = destination / filename
        shutil.copyfile(source / filename, target, follow_symlinks=False)
        os.chmod(target, 0o644)
        written.append(target)
    (destination / "manifest.json").write_bytes(manifest)
    (destination / "NOTICE.md").write_text(NOTICE, encoding="utf-8")
    for name in ("manifest.json", "NOTICE.md"):
        os.chmod(destination / name, 0o644)
    bundle = destination / PUBLIC_DATASET_NAME
    with zipfile.ZipFile(bundle, "x", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=4, allowZip64=True) as z:
        for f in [destination / "NOTICE.md", destination / "manifest.json", *written]:
            zi = zipfile.ZipInfo("apur-paris-grid-500m/" + f.name,
                                 (2026, 10, 17, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = (0o100644 << 16)
            with f.open("rb") as inp, z.open(zi, "w", force_zip64=True) as out:
                shutil.copyfileobj(inp, out, length=512 * 1024)
    os.chmod(bundle, 0o644)
    with zipfile.ZipFile(bundle) as z:
        if z.testzip() is not None or len(z.namelist()) != 458:
            raise ValueError("Derivative download ZIP CRC/count mismatch")
    return {
        "public_manifest_sha256": sha_bytes(manifest),
        "zip_sha256": sha_bytes(bundle.read_bytes()),
        "zip_size": bundle.stat().st_size,
        "cell_count": len(written),
        "unique_features": 128089,
        "source_manifest_sha256": PRIVATE_MANIFEST_SHA,
    }
