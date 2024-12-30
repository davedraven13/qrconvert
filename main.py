import qrcode
from pyzbar.pyzbar import decode
from PIL import Image
import os
import base64
import cv2


def split_file(file_path, chunk_size):
    global before_conv 
    with open(file_path, 'rb') as f:
        data = f.read()
    data_in_chunks_raw = [base64.b64encode(data[i:i + chunk_size]) for i in range(0, len(data), chunk_size)] 

    print(f"Number of chunks is {len(data_in_chunks_raw)}")
    return data_in_chunks_raw

def create_qr(data_chunk, index, output_folder):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=5,
    )
    
    qr.add_data(data_chunk, optimize = 0)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"{output_folder}/{index}.png")

def decode_qrs(frame_folder, result_file_name):
    global after_conv
    data = b""  
    for frame in sorted(os.listdir(frame_folder), key= lambda num: int(num.split(".")[0])):
        if frame.endswith(".png"):
            img = Image.open(os.path.join(frame_folder, frame))
            decoded_objects = decode(img)
            for obj in decoded_objects:
                raw_data =  base64.b64decode(obj.data)
                data += raw_data 

    with open(result_file_name, "wb") as f:
        f.write(data)  # Write the accumulated binary data to a file

def code_to_qrs(file_name):
    if not os.path.isfile(file_name):
        print(f"File '{file_name}' not found!")
        return

    output_folder = "qr_output"
    os.makedirs(output_folder, exist_ok=True)
    chunks = split_file(file_name, 512)  # 64-byte chunks
    total = len(chunks)
    for i, chunk in enumerate(chunks):
        create_qr(chunk, i, output_folder)
        if i % 100 == 0:
            print(f"{i} is done out of {total}")

def images_to_video(image_folder, output_video, fps=30, frame_suspense = 5):
    images = [img for img in sorted(os.listdir(image_folder), key = lambda num: int(num.split(".")[0])) if img.endswith(".png") or img.endswith(".jpg")]
    print(f"no of pictures found {len(images)}")
    frame = cv2.imread(os.path.join(image_folder, images[0]))

    # Get the width and height of the images
    height, width, layers = frame.shape
    size_orig = (width, height)
    
    # Define the codec and create VideoWriter object
    out = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'mp4v'), fps, size_orig)

    for i,image in enumerate(images):
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path)
        height, width, layers = frame.shape
        size = (width, height)
        if size!=size_orig:
            frame = cv2.resize(frame, size_orig )

        if i==0:
            for _ in range(frame_suspense+fps*4):
                res = out.write(frame) 
        else:    
            for _ in range(frame_suspense):
                res = out.write(frame) 


    out.release()
    cv2.destroyAllWindows()
    print(f"Video saved as {output_video}")

def entry_point():
    file_name = "Programming_as_Theory_Building.pdf"
    output_folder = "qr_output"
    result_file = "result.pdf"
    print("start things")

    # Encode file into QR codes
    code_to_qrs(file_name)

    # Decode QR codes back into file
    decode_qrs(output_folder, result_file)

    # Usage example
    output_video = 'output_video.mp4'
    images_to_video(output_folder, output_video, frame_suspense=2)


if __name__ == "__main__":
    entry_point()