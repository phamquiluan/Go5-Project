

class OCRModel:
    def __init__(self):
        # TODO: khoi tao model
        pass

    def process(self, image):
        # TODO process here
        return "abc"

def get_text_line_image():
    # TODO:
    pass

def main():
    import cv2
    # input
    image = cv2.imread("../sample.jpg")
    text_line_list = [{
        "xmin": 0,
        "ymin": 0,
        "xmax": 0,
        "ymax": 0,
    }]


    model = OCRModel()
    
    output_list = []

    for text_line in text_line_list:
        text_line_image = get_text_line_image(image, text_line)
        output = model.process(text_line_image)
        output_list.append(output)

if __name__ == "__main__":
    main()
