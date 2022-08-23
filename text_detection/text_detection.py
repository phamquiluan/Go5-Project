
import os
from helper import run_inference

IMG_PATH = '/home/an/image/Screenshot11.png'
OUTPUT_DIR = "/home/an/cropped_img/"

#path to mmocr library 
MMOCR_PATH = "/home/an/test_folder/mmocr"
os.chdir(MMOCR_PATH)

    config_dir = os.path.join(os.getcwd(), 'configs/')
    mmocr = MMOCR(det='FCE_CTW_DCNv2', config_dir=config_dir, recog=None)
    img_dir = ''
    
    results = mmocr.readtext(
       img_dir)
    results = results[0]["boundary_result"]
    results = list(map(list_process, results))
    return results

main()
run_inference(IMG_PATH, OUTPUT_DIR)
