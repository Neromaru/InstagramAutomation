from PIL import Image, ImageOps
import requests

def create_post(a_file):
    with open(a_file, 'r') as f:
        post_url = f.readline().strip()
        post_text = f.read()
    im_file_name = post_url.split('/')[-1]
    im_res = requests.get(post_url)
    if im_res.status_code != 200:
        print('Failed to get image from URL, please check the text file')
        return False
    with open(im_file_name, 'wb') as f:
        f.write(im_res.content)

    im_file_name_wo_ext = im_file_name.split('.')[0]
    ext = im_file_name.split('.')[1]
    image = Image.open(im_file_name)
    (width, height) = image.size
    # We check the aspect ratio. Instagram only accepts some aspect ratios.
    if width * 1.25 < height:
        image = ImageOps.fit(image, (width, int(width * 1.25)))
        resized_filename = im_file_name_wo_ext + '_resized.' + ext
        image.save(resized_filename)
        print('resized image')
