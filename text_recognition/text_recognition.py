from crnn_pytorch.src.model import CRNN
import torch
import cv2
from crnn_pytorch.src.predict import predict
from crnn_pytorch.src.dataset import CustomDataset
from torch.utils.data import DataLoader
from crnn_pytorch.src.dataset import Synth90kDataset, synth90k_collate_fn
from crnn_pytorch.src.config import common_config as config


class OCRModel:
    def __init__(self):
        # TODO: khoi tao model
        num_class = len(Synth90kDataset.LABEL2CHAR) + 1
        self.crnn = CRNN(1, img_height=config['img_height'], img_width=config['img_width'], num_class=num_class)
        self.crnn.load_state_dict(torch.load('/home/daitama/test/crnn-pytorch/checkpoints/crnn_synth90k.pt', map_location=torch.device('cpu')))

    def process(self, image):
        # TODO process here
        dataset = CustomDataset(data=[image], width=100, height=32)
        dataloader = DataLoader(dataset, batch_size=1)
        CHARS = '0123456789abcdefghijklmnopqrstuvwxyz'
        CHAR2LABEL = {char: i + 1 for i, char in enumerate(CHARS)}
        LABEL2CHAR = {label: char for char, label in CHAR2LABEL.items()}
        pred = predict(self.crnn, dataloader=dataloader, label2char=LABEL2CHAR, decode_method='beam_search', beam_size=10)
        return pred[0]

def get_text_line_image(image, text_line):
    # TODO:
    new_img = image[text_line['xmin']:text_line['xmax'], text_line['ymin']:text_line['ymax'], :]
    return new_img

def main():
    # input
    image = cv2.imread("/home/daitama/Desktop/hello/Go5-Project/text_recognition/crnn_pytorch/demo/78_Novel_52433.jpg")
    text_line_list = [{
        "xmin": 0,
        "ymin": 0,
        "xmax": image.shape[0],
        "ymax": image.shape[1],
    }]
    print(image.shape)

    model = OCRModel()
    
    output_list = []

    for text_line in text_line_list:
        text_line_image = get_text_line_image(image, text_line)
        output = model.process(text_line_image)
        output_list.append(output)
    print(''.join(output_list[0]))

if __name__ == "__main__":
    main()