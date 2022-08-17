import os

class TextRecognizer:
    instance = None

    def __init__(self, weights_path = None):
        # init your model here
        if weights_path is None:
            weights_path = os.path.join(
                os.path.dirname(__file__),
                "weight.pth"
            ) 
            assert os.path.exists(weights_path), weights_path
        
        # TODO: change this
        self.model = lambda x, y: [{
            "name": "text",
            "xmin": 100,
            "ymin": 100,
            "xmax": 200,
            "ymax": 200,
            "text": "hello world!"
        }]

    def process(self, image, text_list : list):
        output = self.model(image, text_list)
        return output

    @classmethod
    def get_unique_instance(cls):
        if cls.instance is None:
            # initialize instance
            cls.instance = cls()
        return cls.instance



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
