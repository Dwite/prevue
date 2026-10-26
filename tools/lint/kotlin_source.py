"""Kotlin 소스를 규칙이 읽을 수 있게 가린다 — 문자열 · 주석의 내용을 공백으로 바꾸고 줄 · 열은 그대로 둔다.

파서가 아니다. 규칙이 정규식으로 코드만 보게 하고, 주석이 걸친 줄을 근사한다.
"""

import re

CODE, STR, RAW = 0, 1, 2


def mask(text, starts=None):
    """(code, comment_lines) — code 는 문자열 · 주석의 내용을 공백으로 가린 같은 길이의 텍스트(따옴표는 남긴다).
    starts 를 주면 줄마다 주석이 처음 시작하는 열을 채운다(블록 주석이 이어지는 줄은 0)."""
    starts = {} if starts is None else starts
    out = list(text)
    comment_lines = set()
    n = len(text)
    stack = [[CODE, 0]]  # [종류, 템플릿 안 중괄호 깊이]
    i = 0
    line = 1

    def blank(a, b):
        for k in range(a, min(b, n)):
            if out[k] != "\n":
                out[k] = " "

    while i < n:
        c = text[i]
        kind = stack[-1][0]
        if kind == CODE:
            if text.startswith("//", i):
                e = text.find("\n", i)
                e = n if e < 0 else e
                blank(i, e)
                comment_lines.add(line)
                starts.setdefault(line, i - (text.rfind("\n", 0, i) + 1))
                i = e
                continue
            if text.startswith("/*", i):
                e = text.find("*/", i + 2)
                e = n if e < 0 else e + 2
                span = text.count("\n", i, e)
                comment_lines.update(range(line, line + span + 1))
                starts.setdefault(line, i - (text.rfind("\n", 0, i) + 1))
                for more in range(line + 1, line + span + 1):
                    starts.setdefault(more, 0)
                blank(i, e)
                line += span
                i = e
                continue
            if text.startswith('"""', i):
                stack.append([RAW, 0])
                i += 3
                continue
            if c == '"':
                stack.append([STR, 0])
                i += 1
                continue
            if c == "'":
                e = i + 1
                while e < n and text[e] not in "'\n":
                    e += 2 if text[e] == "\\" else 1
                blank(i + 1, e)
                i = e if e < n and text[e] == "\n" else e + 1
                continue
            if c == "{" and len(stack) > 1:
                stack[-1][1] += 1
            elif c == "}" and len(stack) > 1:
                if stack[-1][1] == 0:
                    stack.pop()
                    out[i] = " "
                    i += 1
                    continue
                stack[-1][1] -= 1
            if c == "\n":
                line += 1
            i += 1
            continue
        if text.startswith("${", i):
            blank(i, i + 2)
            stack.append([CODE, 0])
            i += 2
            continue
        if kind == RAW and text.startswith('"""', i):
            e = i + 3
            while e < n and text[e] == '"':
                e += 1
            blank(i, e - 3)
            stack.pop()
            i = e
            continue
        if kind == STR:
            if c == "\\":
                blank(i, i + 2)
                i += 2
                continue
            if c == '"' or c == "\n":
                stack.pop()
                if c == "\n":
                    line += 1
                i += 1
                continue
        if c == "\n":
            line += 1
        else:
            out[i] = " "
        i += 1
    return "".join(out), comment_lines

