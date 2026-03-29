#!/usr/bin/env python3
"""HTTP request/response parser and builder."""
import sys

def parse_request(raw):
    lines = raw.split(chr(10)); first = lines[0].split(" ")
    method, path = first[0], first[1] if len(first) > 1 else "/"
    version = first[2] if len(first) > 2 else "HTTP/1.1"
    headers = {}; body_start = 1
    for i, line in enumerate(lines[1:], 1):
        line = line.strip()
        if not line: body_start = i + 1; break
        if ": " in line:
            k, v = line.split(": ", 1); headers[k.lower()] = v
    body = chr(10).join(lines[body_start:]) if body_start < len(lines) else ""
    return {"method": method, "path": path, "version": version, "headers": headers, "body": body}

def parse_response(raw):
    lines = raw.split(chr(10)); first = lines[0].split(" ", 2)
    version = first[0]; status = int(first[1]) if len(first) > 1 else 0
    reason = first[2] if len(first) > 2 else ""
    headers = {}; body_start = 1
    for i, line in enumerate(lines[1:], 1):
        line = line.strip()
        if not line: body_start = i + 1; break
        if ": " in line:
            k, v = line.split(": ", 1); headers[k.lower()] = v
    body = chr(10).join(lines[body_start:]) if body_start < len(lines) else ""
    return {"version": version, "status": status, "reason": reason, "headers": headers, "body": body}

def build_request(method, path, headers=None, body=""):
    NL = chr(10)
    lines = [f"{method} {path} HTTP/1.1"]
    for k, v in (headers or {}).items(): lines.append(f"{k}: {v}")
    if body: lines.append(f"Content-Length: {len(body)}")
    lines.append(""); lines.append(body)
    return NL.join(lines)

def build_response(status, reason="OK", headers=None, body=""):
    NL = chr(10)
    lines = [f"HTTP/1.1 {status} {reason}"]
    for k, v in (headers or {}).items(): lines.append(f"{k}: {v}")
    if body: lines.append(f"Content-Length: {len(body)}")
    lines.append(""); lines.append(body)
    return NL.join(lines)

STATUS_CODES = {200:"OK",201:"Created",204:"No Content",301:"Moved",400:"Bad Request",401:"Unauthorized",403:"Forbidden",404:"Not Found",500:"Internal Server Error"}

def main():
    if len(sys.argv) < 2: print("Usage: http_parser.py <demo|test>"); return
    if sys.argv[1] == "test":
        NL = chr(10)
        req = f"GET /api/users HTTP/1.1{NL}Host: example.com{NL}Accept: application/json{NL}{NL}"
        r = parse_request(req)
        assert r["method"] == "GET"; assert r["path"] == "/api/users"
        assert r["headers"]["host"] == "example.com"
        resp = f"HTTP/1.1 200 OK{NL}Content-Type: text/html{NL}{NL}<h1>Hello</h1>"
        rr = parse_response(resp)
        assert rr["status"] == 200; assert rr["reason"] == "OK"
        assert "<h1>" in rr["body"]
        built = build_request("POST", "/api", {"Content-Type": "application/json"}, '{"key":"val"}')
        assert "POST /api" in built; assert "Content-Length" in built
        br = build_response(404, "Not Found")
        assert "404" in br
        print("All tests passed!")
    else:
        print(build_request("GET", "/", {"Host": "example.com"}))

if __name__ == "__main__": main()
