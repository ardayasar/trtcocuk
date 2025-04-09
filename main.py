import json
import time
import m3u8
import os
from pym3u8downloader import M3U8Downloader

save_to_dir = 'C:\\Users\\buyuk\\Desktop\\trt'

# Load the JSON data from the file
with open('data.json', 'r') as file:
    full = json.loads(file.read())

# Iterate over the dictionary to access keys and values
for key, value in full.items():
    print(f"Key: {key}")
    if not os.path.exists(f'{save_to_dir}\\{key}'):
        os.makedirs(f'{save_to_dir}\\{key}')
        print(f"Directory {save_to_dir}\\{key} created.")

    for episode in value:
        try:
            # print(f"Episode Title: {episode[0]}, M3U8 URL: {episode[1]}")
            if not os.path.exists(f'{save_to_dir}\\{key}\\{episode[0]}.mp4'):

                playlist = m3u8.load(episode[1])

                selected_variant_res = None
                selected_variant_band = 0

                for variant in playlist.playlists:
                    if selected_variant_band < variant.stream_info.bandwidth:
                        selected_variant_res = variant.stream_info.resolution  # Resolution of the video stream (e.g., (1280, 720))
                        selected_variant_band = variant.stream_info.bandwidth  # Bandwidth of the stream (in bits per second)

                downloader = M3U8Downloader(
                    input_file_path=str(episode[1]),
                    output_file_path=f'{save_to_dir}\\{key}\\{episode[0]}.mp4'
                )
                downloader.download_master_playlist(bandwidth=str(selected_variant_band),
                                                    resolution=f'{selected_variant_res[0]}x{selected_variant_res[1]}')

                print(f'Download completed for -> {episode[0]}')

        except Exception as e:
            print(f'Passed: Episode Title: {episode[0]}, M3U8 URL: {episode[1]}')
            time.sleep(10)
