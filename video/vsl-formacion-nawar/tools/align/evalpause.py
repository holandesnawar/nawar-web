"""Check an alignment against the take's real pauses.

Every real pause (>=0.18 s of low energy) should sit at a word boundary that
carries punctuation in the script; every sentence end should have a pause.
Prints the hit rates plus the words that border each pause."""
import json, re, sys

def boundaries(text):
    toks = list(re.finditer(r"[\wÀ-ÿ'’]+", text))
    out = []
    for k, m in enumerate(toks):
        nxt = toks[k + 1].start() if k + 1 < len(toks) else len(text)
        between = text[m.end():nxt]
        out.append(between.strip())
    return out  # punctuation after word k

def main(text_path, al_path, pauses_path, take_idx):
    text = open(text_path, encoding="utf-8").read().strip().replace("\n", " ")
    punct = boundaries(text)
    words = json.load(open(al_path))["words"]
    pauses = json.load(open(pauses_path))[int(take_idx)]["pauses"]
    hits, misses = 0, []
    for a, b in pauses:
        mid = (a + b) / 2
        # boundary k = between word k and k+1 closest to pause middle
        best = min(range(len(words) - 1), key=lambda k: abs((words[k]["end"] + words[k + 1]["start"]) / 2 - mid))
        p = punct[best]
        if p and any(c in p for c in ",.;:?!…¿¡"):
            hits += 1
        else:
            misses.append((round(mid, 2), words[best]["text"], words[best + 1]["text"]))
    sent_ends = [k for k, p in enumerate(punct) if any(c in p for c in ".?!…")]
    covered = 0
    for k in sent_ends[:-1]:
        t = (words[k]["end"] + words[k + 1]["start"]) / 2
        if any(a - 0.35 <= t <= b + 0.35 for a, b in pauses):
            covered += 1
    print(f"pause@punct {hits}/{len(pauses)}  sentence-ends-with-pause {covered}/{len(sent_ends)-1}")
    print("  pauses not at punctuation:", misses[:20])

if __name__ == "__main__":
    main(*sys.argv[1:5])
