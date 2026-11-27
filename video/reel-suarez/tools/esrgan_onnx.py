#!/usr/bin/env python3
"""Turns Real-ESRGAN's «realesr-general-x4v3.pth» (SRVGGNetCompact: 64 features, 32 convs, PReLU, ×4 pixel shuffle)
into an ONNX model for onnxruntime, with no PyTorch. The .pth is a zip whose data.pkl is a pickle: it is NOT unpickled
(that could run code from the file). pickletools only lists its opcodes; a tiny interpreter here understands just the
handful a plain state dict uses (strings, ints, tuples, dicts, and the two names torch writes: OrderedDict and
_rebuild_tensor_v2) and reads each tensor's raw bytes from the zip. Anything else stops it.
  python3 tools/esrgan_onnx.py .raw/realesr-general-x4v3.pth .raw/esrgan-x4v3.onnx
"""
import pickletools, sys, zipfile
import numpy as np

ALLOWED_GLOBALS = {("collections", "OrderedDict"), ("torch._utils", "_rebuild_tensor_v2"),
                   ("torch", "FloatStorage"), ("torch", "HalfStorage")}
DTYPES = {"FloatStorage": np.float32, "HalfStorage": np.float16}


def state_dict(path):
    z = zipfile.ZipFile(path)
    pkl = next(n for n in z.namelist() if n.endswith("/data.pkl"))
    root = pkl[: -len("data.pkl")]
    stack, memo, MARK = [], {}, object()

    def pop_mark():
        i = max(k for k, v in enumerate(stack) if v is MARK)
        items = stack[i + 1:]; del stack[i:]
        return items

    for op, arg, _ in pickletools.genops(z.read(pkl)):
        n = op.name
        if n in ("PROTO", "FRAME"):
            continue
        elif n in ("EMPTY_DICT",):
            stack.append({})
        elif n == "EMPTY_TUPLE":
            stack.append(())
        elif n == "EMPTY_LIST":
            stack.append([])
        elif n == "MARK":
            stack.append(MARK)
        elif n in ("BINUNICODE", "SHORT_BINUNICODE", "UNICODE", "BININT", "BININT1", "BININT2", "LONG1"):
            stack.append(arg)
        elif n in ("NEWFALSE", "NEWTRUE"):
            stack.append(n == "NEWTRUE")
        elif n == "NONE":
            stack.append(None)
        elif n == "GLOBAL":
            mod, name = arg.split(" ", 1)
            if (mod, name) not in ALLOWED_GLOBALS:
                raise SystemExit(f"unexpected global {mod}.{name}: not a plain state dict")
            stack.append(("GLOBAL", mod, name))
        elif n == "STACK_GLOBAL":
            name = stack.pop(); mod = stack.pop()
            if (mod, name) not in ALLOWED_GLOBALS:
                raise SystemExit(f"unexpected global {mod}.{name}: not a plain state dict")
            stack.append(("GLOBAL", mod, name))
        elif n == "TUPLE":
            stack.append(tuple(pop_mark()))
        elif n in ("TUPLE1", "TUPLE2", "TUPLE3"):
            k = int(n[-1]); items = stack[-k:]; del stack[-k:]; stack.append(tuple(items))
        elif n in ("BINPUT", "LONG_BINPUT"):
            memo[arg] = stack[-1]
        elif n == "MEMOIZE":
            memo[len(memo)] = stack[-1]
        elif n in ("BINGET", "LONG_BINGET"):
            stack.append(memo[arg])
        elif n == "BINPERSID":
            pid = stack.pop()                                   # ('storage', FloatStorage, key, location, numel)
            stack.append(("STORAGE", DTYPES[pid[1][2]], pid[2]))
        elif n == "REDUCE":
            args = stack.pop(); fn = stack.pop()
            if fn == ("GLOBAL", "collections", "OrderedDict"):
                stack.append({})
            elif fn == ("GLOBAL", "torch._utils", "_rebuild_tensor_v2"):
                (_, dt, key), offset, size, stride = args[:4]
                buf = np.frombuffer(z.read(f"{root}data/{key}"), dt)
                arr = np.lib.stride_tricks.as_strided(buf[offset:], shape=size, strides=[s * buf.itemsize for s in stride])
                stack.append(np.array(arr, np.float32))
            else:
                raise SystemExit(f"unexpected call {fn}")
        elif n == "SETITEM":
            v = stack.pop(); k = stack.pop(); stack[-1][k] = v
        elif n == "SETITEMS":
            items = pop_mark(); d = stack[-1]
            for k, v in zip(items[::2], items[1::2]):
                d[k] = v
        elif n == "APPENDS":
            items = pop_mark(); stack[-1].extend(items)
        elif n == "BUILD":
            stack.pop()                                         # an object's state (empty for these): ignored
        elif n == "STOP":
            break
        else:
            raise SystemExit(f"unexpected opcode {n}")
    sd = stack[-1]
    return sd.get("params", sd.get("params_ema", sd))


def build(sd, out):
    import onnx
    from onnx import helper, numpy_helper, TensorProto
    nodes, inits = [], []
    def W(name, arr):
        inits.append(numpy_helper.from_array(np.asarray(arr, np.float32), name)); return name
    convs = sorted({int(k.split(".")[1]) for k in sd if k.startswith("body.")})
    x = "input"
    for i in convs:
        w, b = sd.get(f"body.{i}.weight"), sd.get(f"body.{i}.bias")
        if w is not None and w.ndim == 4:                      # a conv
            y = f"c{i}"
            nodes.append(helper.make_node("Conv", [x, W(f"w{i}", w), W(f"b{i}", b)], [y], pads=[1, 1, 1, 1]))
            x = y
        elif w is not None:                                    # a PReLU (num_parameters = 64)
            y = f"a{i}"
            nodes.append(helper.make_node("PRelu", [x, W(f"p{i}", w.reshape(-1, 1, 1))], [y]))
            x = y
    nodes.append(helper.make_node("DepthToSpace", [x], ["ps"], blocksize=4, mode="CRD"))
    nodes.append(helper.make_node("Resize", ["input", "", W("scales", [1, 1, 4, 4])], ["up"], mode="nearest"))
    nodes.append(helper.make_node("Add", ["ps", "up"], ["output"]))
    g = helper.make_graph(nodes, "realesr-general-x4v3",
                          [helper.make_tensor_value_info("input", TensorProto.FLOAT, [1, 3, None, None])],
                          [helper.make_tensor_value_info("output", TensorProto.FLOAT, [1, 3, None, None])], inits)
    m = helper.make_model(g, opset_imports=[helper.make_opsetid("", 13)]); m.ir_version = 8   # what onnxruntime 1.x reads
    onnx.checker.check_model(m); onnx.save(m, out)
    print(f"{out}: {len(convs)} body layers, {sum(a.size for a in sd.values()):,} weights")


if __name__ == "__main__":
    build(state_dict(sys.argv[1]), sys.argv[2])
