from roboflow import Roboflow
import os
rf = Roboflow(api_key="7ldwT6oeFy8rCd3QCntI")
# ganti workspace/project sesuai dataset lo
project = rf.workspace("cath-oxqmx").project("vehicle-detection-0dzfu-k9qkx")
# format: "yolov8" untuk bbox, "yolov8-pose" untuk keypoints/pose
project.version(1).download("yolov8", location="dataset")
