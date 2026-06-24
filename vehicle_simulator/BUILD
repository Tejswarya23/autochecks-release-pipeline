load("@rules_python//python:defs.bzl", "py_library", "py_test")

py_library(
    name = "sensor",
    srcs = ["sensor.py"],
    imports = [".."],
    visibility = ["//visibility:public"],
)

py_test(
    name = "sensor_test",
    srcs = ["sensor_test.py"],
    imports = [".."],
    deps = [":sensor"],
)
