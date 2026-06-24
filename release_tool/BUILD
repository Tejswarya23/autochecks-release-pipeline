load("@rules_python//python:defs.bzl", "py_binary", "py_test")

py_binary(
    name = "release",
    srcs = ["release.py"],
    deps = ["//config:settings"],
)

py_test(
    name = "release_test",
    srcs = ["release_test.py"],
    deps = [":release"],
)
