#!/usr/bin/env python3
"""모듈의 @Preview 파일 목록을 데몬에 하나씩 show해 성공률과 실패 종류를 센다(FR-12 분류 검증, 기획서의 core:ui 43개 측정).

사용법: survey.py <port> <파일 목록 txt> [결과 json]
"""
import json, sys, time, urllib.request

port, list_path = sys.argv[1], sys.argv[2]
out_path = sys.argv[3] if len(sys.argv) > 3 else None
base = f"http://127.0.0.1:{port}"


def post(path, body):
    req = urllib.request.Request(base + path, json.dumps(body).encode(), {"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return json.load(e)


rows = []
files = [l.strip() for l in open(list_path) if l.strip()]
for f in files:
    previews = post("/previews", {"file": f}).get("previews", [])
    if not previews:
        rows.append({"file": f, "previewId": None, "ok": False, "failure": "NO_PREVIEW_FOUND", "ms": 0})
        continue
    for p in previews:
        t = time.time()
        r = post("/show", {"target": f, "index": p["index"], "by": "survey"})
        rows.append({
            "file": f, "previewId": p["previewId"], "params": p.get("params"), "ok": r.get("ok"), "failure": r.get("failure") or r.get("error"),
            "message": (r.get("message") or "")[:400], "ms": int((time.time() - t) * 1000), "renderMs": r.get("renderMs"),
            "size": [r.get("width"), r.get("height")],
        })
        short = f.split("/src/")[-1]
        print(f"{'OK ' if r.get('ok') else 'ERR'} {rows[-1]['ms']:5d}ms {short}#{p['index']} {p['previewId']} {rows[-1]['failure'] or ''}")

ok = sum(1 for r in rows if r["ok"])
kinds = {}
for r in rows:
    if not r["ok"]:
        kinds[r["failure"]] = kinds.get(r["failure"], 0) + 1
print(f"\n프리뷰 {len(rows)}개 / 파일 {len(files)}개 — 성공 {ok} ({ok * 100 // max(1, len(rows))}%), 실패 {kinds}")
if out_path:
    json.dump(rows, open(out_path, "w"), ensure_ascii=False, indent=1)
    print("→", out_path)
