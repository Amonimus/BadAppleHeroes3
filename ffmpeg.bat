@echo off
start ffmpeg -framerate 60 -i result/f%%d.png export/render.mp4