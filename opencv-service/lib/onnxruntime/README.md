# ONNX runtime

Since the ONNX runtime is not prebuilt for 32-bit arm (arm/v7), we had to build it
from source in an arm/v7 Ubuntu container.

You can refer to the installation instruction [here](https://onnxruntime.ai/docs/build/inferencing.html).

The resulting shared library has been put under `opencv-service/lib/onnxruntime/arm32/lib`.
