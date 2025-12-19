# Copyright 2025 Bytedance Ltd. and/or its affiliates.
# SPDX-License-Identifier: Apache-2.0

import io
import base64
import tempfile
import os
import cv2
from torchcodec.decoders import VideoDecoder
import numpy as np
from PIL import Image


def resize_video(image, tokens_per_image, patch_size=28):
    width, height = image.size
    target_size = patch_size * patch_size * tokens_per_image
    scale_factor = (target_size / (width * height))**0.5
    new_width = round(width * scale_factor)
    new_height = round(height * scale_factor)
    return image.resize((new_width, new_height))


def frames_to_base64_list(frames: list, tokens_per_image):
    base64_list = []
    # Convert decord NDArray to numpy array
    for frame in frames:
        # Convert numpy array to PIL Image
        img = Image.fromarray(frame)
        # Save to BytesIO as JPEG
        img = resize_video(img, tokens_per_image, patch_size=14 * 3)
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG")
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
        base64_list.append(img_str)
        buffer.close()
    return base64_list


def process_video(video_bytes: bytes,
                  sampling_fps: int = 1,
                  max_frames: int = 1280,
                  max_video_length: int = 81920):

    # predefined tokens per frame
    token_sets = [64, 128, 192, 256, 320, 384]

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video_file:
        temp_video_file.write(video_bytes)
        temp_video_path = temp_video_file.name

    try:
        cap = cv2.VideoCapture(temp_video_path)
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()

        video_stream = io.BytesIO(video_bytes)
        vr = VideoDecoder(video_stream.getvalue(), dimension_order="NHWC")
        total_frame_num = len(vr)
        duration = total_frame_num / video_fps

        sampling_num_frames = int(duration) * sampling_fps
        # if you set max_frames to a smaller value, it will be used
        sampling_num_frames = min(sampling_num_frames, max_frames)
        max_token = 64

        # dynamic tokens per frame, based on max_video_length
        for token in token_sets:
            if token * sampling_num_frames <= max_video_length:
                max_token = token
        if max_token * sampling_num_frames > max_video_length:
            sampling_num_frames = int(max_video_length / max_token)

        frame_indices = np.linspace(0, total_frame_num - 1, sampling_num_frames)
        frame_indices = [round(x) for x in frame_indices]

        timestamps = [frame_index / video_fps for frame_index in frame_indices]
        print("[video] {} second video, sampling {} frames, {} tokens per frame".
              format(round(duration, 1), len(frame_indices), max_token))
        # Get sampled frames
        frames = vr.get_frames_at(frame_indices).data.numpy()
        video_base64_list = frames_to_base64_list(frames, max_token)

        del vr
        return video_base64_list, timestamps, frame_indices
    finally:
        os.remove(temp_video_path)


def sample_frames_from_video_bytes(
    video_bytes: bytes,
    start_time: float,
    end_time: float,
    sample_fps: int = 1,
    tokens_per_image: int = 256,
) -> tuple:
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video_file:
        temp_video_file.write(video_bytes)
        temp_video_path = temp_video_file.name

    try:
        cap = cv2.VideoCapture(temp_video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()

        video_buffer = io.BytesIO(video_bytes)
        vr = VideoDecoder(video_buffer.getvalue(), dimension_order="NHWC")
        total_frame_num = len(vr)
        duration = total_frame_num / fps

        start_time = max(0.0, float(start_time))
        end_time = float(duration) if end_time is None else min(
            float(end_time), float(duration))
        if end_time < start_time:
            end_time = start_time

        # sampling frames
        start_frame = min(int(start_time * fps), total_frame_num - 1)
        end_frame = min(int(end_time * fps), total_frame_num)
        total_frame_num = end_frame - start_frame

        # Update duration based on the truncated video
        duration = total_frame_num / fps if total_frame_num > 0 else 0.0

        frame_interval = max(1, int(round(fps / sample_fps)))
        frame_indices = list(range(start_frame, end_frame, frame_interval))
        # Ensure frame_indices is not empty
        if not frame_indices:
            frame_indices = [start_frame] if start_frame <= end_frame else []
        frame_timestamps = [round(x / fps, 1) for x in frame_indices]

        # Get sampled frames
        frames = vr.get_frames_at(frame_indices).data.numpy()
        video_base64_list = frames_to_base64_list(
            frames, tokens_per_image)  # Convert to bytes list

        del vr
        return video_base64_list, frame_timestamps
    finally:
        os.remove(temp_video_path)
