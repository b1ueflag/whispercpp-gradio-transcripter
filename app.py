import subprocess
import os
import sys
import gradio as gr
import shutil

def extract_audio(video_file, audio_file):
    cmd = f"ffmpeg -i {video_file} -vn -acodec pcm_s16le -ar 16000 -ac 1 {audio_file}"
    subprocess.run(cmd, shell=True, check=True)

def translate(file):
    video_file = "input.mp4"
    audio_file = "input.wav"
    output_file = "output.txt"

    # Save the uploaded file
    shutil.copy(file, video_file)

    # Extract the audio from the video
    extract_audio(video_file, audio_file)

    # Call the whisper binary
    cmd = f"./whisper.cpp/build/bin/main -m ./whisper.cpp/models/ggml-base.bin -f {audio_file} -l ja > {output_file}"
    subprocess.run(cmd, shell=True, check=True)

    # Read the output file
    with open(output_file, "r") as f:
        transcript = f.read()

    # Clean up
    os.remove(video_file)
    os.remove(audio_file)
    os.remove(output_file)

    return transcript

iface = gr.Interface(fn=translate, inputs=gr.inputs.Video(), outputs="text", analytics_enabled=False)
iface.launch(debug=True)
