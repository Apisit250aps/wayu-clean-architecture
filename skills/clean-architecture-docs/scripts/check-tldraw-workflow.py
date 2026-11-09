"""Check the file structure and cross-view references of an HMS workflow set."""

import json
import re
import sys
from collections import Counter
from pathlib import Path


def label(node):
    separator = "\n" if node.get("type") == "doc" else ""
    return node.get("text", separator.join(label(child) for child in node.get("content", [])))


def read_canvas(path, frame_pattern, errors):
    document = json.loads(path.read_text(encoding="utf-8"))
    if document.get("tldrawFileFormatVersion") != 1 or not isinstance(document.get("schema"), dict):
        raise ValueError(f"{path.name}: expected legacy .tldr version 1 with a schema")
    records = document["records"]
    ids = Counter(record["id"] for record in records)
    errors.extend(f"{path.name}: duplicate record {key}" for key, count in ids.items() if count > 1)
    shapes = {record["id"]: record for record in records if record["typeName"] == "shape"}
    frames = {key for key, shape in shapes.items() if shape["type"] == "frame"}
    if not frames or any(not re.fullmatch(frame_pattern, key) for key in frames):
        errors.append(f"{path.name}: missing frames or frame IDs belong to the wrong view")

    bindings = Counter()
    for record in records:
        if record["typeName"] != "binding" or record.get("type") != "arrow":
            continue
        source, target = record["fromId"], record["toId"]
        if shapes.get(source, {}).get("type") != "arrow" or target not in shapes:
            errors.append(f"{path.name}: invalid binding {record['id']}")
        bindings[source, record["props"]["terminal"]] += 1

    texts = []
    for key, shape in shapes.items():
        props = shape["props"]
        if shape["parentId"] not in ids:
            errors.append(f"{path.name}: missing parent for {key}")
        if shape["type"] == "arrow" and any(bindings[key, end] != 1 for end in ("start", "end")):
            errors.append(f"{path.name}: expected a binding at both ends of {key}")
        if props.get("url"):
            errors.append(f"{path.name}: use text pointers instead of a URL on {key}")
        texts.append((key, props.get("text") or label(props.get("richText", {}))))
    return shapes, frames, texts


def check(directory):
    module = directory.name
    errors = []
    views = {
        "flow": ("1", r"shape:p0[a-z]?"),
        "business": ("2", r"shape:p[1-9]\d*[a-z]?"),
        "endpoint": ("3", r"shape:e[1-6][a-z]?"),
    }
    if not (directory / "README.md").is_file():
        errors.append("Missing README.md")
    for path in directory.glob("*.tldraw"):
        errors.append(f"{path.name}: use separate legacy .tldr files for the HMS workflow")
    canvases = {}
    for view, (order, pattern) in views.items():
        path = directory / f"{order}.{module}-{view}.tldr"
        try:
            canvases[view] = read_canvas(path, pattern, errors)
        except (OSError, ValueError, TypeError, KeyError, AttributeError) as error:
            errors.append(f"{path.name}: {error}")

    if len(canvases) != len(views):
        return errors

    _, flow_frames, flow_text = canvases["flow"]
    business_shapes, business_frames, business_text = canvases["business"]
    endpoint_shapes, endpoint_frames, _ = canvases["endpoint"]
    if "shape:p0" not in flow_frames:
        errors.append("Flow is missing P0")
    covered = set()
    for box, text in flow_text:
        if "ดูต่อ 2." not in text:
            continue
        pointer = re.search(rf"ดูต่อ 2\.{re.escape(module)}-business\s+(.+)", text)
        destinations = re.findall(r"\bP[1-9]\d*[a-z]?\b", pointer[1]) if pointer else []
        if not destinations:
            errors.append(f"Flow {box}: missing Business frame in pointer")
        for frame in destinations:
            frame_id = "shape:" + frame.lower()
            if frame_id not in business_frames:
                errors.append(f"Flow {box}: unknown Business frame {frame}")
            covered.add(frame_id)
    errors.extend(f"Business frame has no Flow pointer: {frame}" for frame in sorted(business_frames - covered))

    business_with_pointers = set()
    for box, text in business_text:
        if "ดูต่อ 3." not in text:
            continue
        business_with_pointers.add(business_shapes[box]["parentId"])
        pointer = re.search(rf"ดูต่อ 3\.{re.escape(module)}-endpoint\s+(.+)", text)
        destinations = re.findall(r"\b(E[1-6][a-z]?)(?:\s+สาย\s+(\d+(?:\s*,\s*\d+)*))?", pointer[1]) if pointer else []
        if not destinations:
            errors.append(f"Business {box}: missing Endpoint frame in pointer")
        for frame, paths in destinations:
            frame_id = "shape:" + frame.lower()
            if frame_id not in endpoint_frames or not paths:
                errors.append(f"Business {box}: expected an existing Endpoint frame and path number for {frame}")
                continue
            for number in re.findall(r"\d+", paths):
                start = endpoint_shapes.get(f"{frame_id}-box-s{number}")
                if not start or start["parentId"] != frame_id:
                    errors.append(f"Business {box}: unknown Endpoint path {frame} สาย {number}")
    for frame in sorted(business_frames - business_with_pointers):
        errors.append(f"Business frame has no Endpoint pointer: {frame}")
    return errors


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: check-tldraw-workflow.py docs/workflow/<module>")
    issues = check(Path(sys.argv[1]))
    if issues:
        sys.exit("\n".join(issues))
    print("Workflow file structure, frames, bindings, and pointers passed.")
