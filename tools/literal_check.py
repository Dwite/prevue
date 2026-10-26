#!/usr/bin/env python3
"""리터럴 빠른 경로(D-67) 그림 대조 — 컴파일 없이 값을 넣은 그림이 컴파일한 그림과 같은가, 로더가 바뀌어도 값이 남는가. 실행: python3 tools/literal_check.py

진짜 데몬 · 상주 컴파일러 · layoutlib으로 nowinandroid `ForYouScreen.kt`(25장)의 `contentPadding`을 바꿔 가며 보드 전부의 PNG를 견준다.
단위 테스트는 가짜 렌더러라 엔진의 장부(새 로더마다 다시 넣는 값)와 컴파일러가 단 자리를 못 본다 — 렌더러 · Compose 판올림이나 이 경로를 고친 뒤 돌린다.
격리는 `nfr_bench.py`와 같다(복사본 `.cache/spike/nfr/`를 `--watch`, 덤프는 `.cache/nfr/`). 하나라도 실패하면 종료 1.
"""

import argparse
import hashlib
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nfr_bench as N  # noqa: E402

SNIP = "contentPadding = PaddingValues(16.dp)"
OTHER = "package com.google.samples.apps.nowinandroid.feature.foryou.impl\n\nfun literalCheckOther(): Int = 1\n"


class Check:
    def __init__(self):
        a = argparse.Namespace(
            repo=N.NIA,
            file=N.NIA + "/feature/foryou/impl/src/main/kotlin/com/google/samples/apps/nowinandroid/feature/foryou/impl/ForYouScreen.kt",
            other=N.NIA + "/core/ui/src/main/kotlin/com/google/samples/apps/nowinandroid/core/ui/NewsResourceCard.kt",
            dump="feature_foryou_impl-demoDebug.json", resources_from="app-demoDebug.json", port=0, cold=1, saves=0,
            interval=1.5, switches=0, rounds=0, idle=0, tab_rounds=0, skip="", literal_at="", resource_at="", values="")
        self.b = N.Bench(a)
        # 새로 생긴 파일은 저장 → 화면을 타지 않는다(빠른 열기 목록만) — 띄우기 전에 두고 나중에 고친다.
        self.other = os.path.join(self.b.spike, "LiteralCheckOther.kt")
        self.write(self.other, OTHER)
        self.results = []

    def source(self, pad, tail=""):
        return self.b.text.replace(SNIP, "contentPadding = PaddingValues(%d.dp)" % pad, 1) + tail

    @staticmethod
    def write(path, body):
        with open(path, "w", encoding="utf-8") as f:
            f.write(body)

    def board(self):
        """저장한 파일의 보드가 지금 세대로 다 그려질 때까지 기다려 카드마다 PNG 해시 · 트리 해시와 reload 줄을 낸다."""
        off = self.b.offset()
        rc, out, _ = self.b.cli("wait", self.b.file, timeout=90)
        j = json.loads(out)
        if rc != 0 or "cards" not in j:
            sys.exit("wait 실패(%d): %s" % (rc, out[:600]))
        lines, _ = self.b.reload_lines(off)
        # 트리는 견주지 않는다 — 같은 코드를 두 번 컴파일해 그려도 지연 그리드의 화면 밖 노드가 렌더마다 달라(25장 중 9장, 2026-10-06)
        # 빠른 경로와 무관하게 흔들린다. 가리키기의 줄은 클래스의 줄 표에서 오고, 빠른 경로는 클래스도 줄도 바꾸지 않는다.
        return {str(c["index"]): self.sha(c["image"]) for c in j["cards"] if c.get("image")}, lines

    @staticmethod
    def sha(path):
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()[:12]

    def save(self, pad, tail=""):
        self.write(self.b.file, self.source(pad, tail))
        return self.board()

    def check(self, name, ok, detail=""):
        self.results.append(ok)
        print(("통과 " if ok else "실패 ") + name + ("  " + detail if detail else ""))

    def diff(self, x, y):
        return "%d장 중 다른 장 %s" % (len(x), [k for k in x if x[k] != y.get(k)])

    def focus(self):
        r = self.b.post("/focus", {"index": 0, "interactive": True, "by": "literal-check"})
        h = self.sha(r["image"])
        self.b.post("/focus", {"index": 0, "interactive": False, "by": "literal-check"})
        return h

    def run(self):
        fast = lambda lines: any(l.rstrip().endswith(" literals") for l in lines)   # noqa: E731
        self.b.start()
        c40, _ = self.save(40)                                                   # 이 내용으로 처음 컴파일한다
        p80, l = self.save(80)
        self.check("80은 빠른 경로", fast(l), str(l))
        self.check("80은 40과 그림이 다르다", p80 != c40)
        p40, l = self.save(40)
        self.check("빠른 경로 40 == 컴파일 40(보드 전부)", fast(l) and p40 == c40, self.diff(p40, c40))
        c80, _ = self.save(80, "\n// compile\n")                                # 코드가 바뀌어 컴파일한다
        self.check("컴파일 80 == 빠른 경로 80(보드 전부)", c80 == p80, self.diff(c80, p80))
        p120, l = self.save(120, "\n// compile\n")
        self.check("120은 빠른 경로", fast(l), str(l))
        # 다른 파일을 컴파일해 세대(로더)를 바꾼다 — 넣어 둔 120이 새 로더에도 들어가야 한다.
        off = self.b.offset()
        self.write(self.other, OTHER + "// changed\n")
        for _ in range(300):
            if any("LiteralCheckOther" in x for x in self.b.reload_lines(off)[0]):
                break
            time.sleep(0.1)
        after, _ = self.board()
        self.check("다른 파일을 컴파일한 뒤(새 로더)에도 120", after == p120, self.diff(after, p120))
        on_fast = self.focus()                                                   # 인터랙티브는 사설 로더다
        c120, _ = self.save(120, "\n// compile 2\n")
        self.check("컴파일 120 == 빠른 경로 120(보드 전부)", c120 == p120, self.diff(c120, p120))
        self.check("인터랙티브 진입(사설 로더): 빠른 경로 == 컴파일", on_fast == self.focus())


def main():
    c = Check()
    try:
        c.run()
    finally:
        c.b.stop()
        import shutil
        shutil.rmtree(c.b.spike, ignore_errors=True)
    print("결과: %d/%d 통과" % (sum(c.results), len(c.results)))
    sys.exit(0 if all(c.results) else 1)


if __name__ == "__main__":
    main()
