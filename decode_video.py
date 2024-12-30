import cv2
import os
from pyzbar.pyzbar import decode
from PIL import Image
import base64
import time

def video_to_images_alt2(video_path, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Save the frame as an image
        frame_filename = os.path.join(output_folder, f"{frame_count}.png")
        cv2.imwrite(frame_filename, frame)
        frame_count += 1

    cap.release()
    print(f"Extracted {frame_count} frames from {video_path}")

def video_to_images(video_path, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"number of framews is {length}")
    frame_count = 0
    for _ in range(length):
        ret, frame = cap.read()
        frame_filename = os.path.join(output_folder, f"{frame_count}.png")
        cv2.imwrite(frame_filename, frame)
        frame_count += 1

    cap.release()
    print(f"Extracted {frame_count} frames from {video_path}")


def video_to_images_alt(input_loc, output_loc):
    """Function to extract frames from input video file
    and save them as separate frames in an output directory.
    Args:
        input_loc: Input video file.
        output_loc: Output directory to save the frames.
    Returns:
        None
    """
    try:
        os.mkdir(output_loc)
    except OSError:
        pass
    # Log the time
    time_start = time.time()
    # Start capturing the feed
    cap = cv2.VideoCapture(input_loc)
    # Find the number of frames
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    print ("Number of frames: ", video_length)
    count = 0
    print ("Converting video..\n")
    # Start converting the video
    while cap.isOpened():
        # Extract the frame
        ret, frame = cap.read()
        if not ret:
            continue
        # Write the results back to output location.
        cv2.imwrite(output_loc + "/%#05d.jpg" % (count+1), frame)
        count = count + 1
        # If there are no more frames left
        if (count > (video_length-1)):
            # Log the time again
            time_end = time.time()
            # Release the feed
            cap.release()
            # Print stats
            print ("Done extracting frames.\n%d frames extracted" % count)
            print ("It took %d seconds forconversion." % (time_end-time_start))
            break

def parse_images(image_folder):
    images = [img for img in sorted(os.listdir(image_folder), key = lambda num: int(num.split(".")[0])) if img.endswith(".png") or img.endswith(".jpg")]
    raw_data_previous = None
    data = b''
    num_of_distinct_chunks = 0
    for img_name in images:
        print(img_name)
        img = Image.open(os.path.join(image_folder, img_name))
        decoded_objects = decode(img)
        for obj in decoded_objects:
            raw_data =  base64.b64decode(obj.data)
            if raw_data != raw_data_previous or raw_data_previous == None:
                num_of_distinct_chunks+=1
                raw_data_previous = raw_data
                data += raw_data 

    print(f"no of distinct chunks found is {num_of_distinct_chunks}")
    
    with open("reuslt_file.pdf", "wb") as f:
        f.write(data)  # Write the accumulated binary data to a file


         
if __name__ == "__main__":
    # Usage example
    video_path = 'VID_20241230_144417.mp4'  # Replace with the path to your video file
    output_folder = 'output_frames'
    video_to_images(video_path, output_folder)
    parse_images(output_folder)
