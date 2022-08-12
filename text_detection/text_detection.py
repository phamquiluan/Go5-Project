def list_process(element):
    element.pop()
    x = element[0::2]
    y = element[1::2]
    x_min = min(x)
    x_max = max(x)
    y_min = min(y)
    y_max = max(y)
    element = dict()
    element["xmin"] = x_min
    element["ymin"] = y_min
    element["xmax"] = x_max
    element["ymax"] = y_max
    return element


def main():
    from mmocr.utils.ocr import MMOCR

    import os
    os.chdir("mmocr")

    config_dir = os.path.join(os.getcwd(), 'configs/')
    mmocr = MMOCR(det='FCE_CTW_DCNv2', config_dir=config_dir, recog=None)
    img_dir = ''
    
    results = mmocr.readtext(
       img_dir)
    results = results[0]["boundary_result"]
    results = list(map(list_process, results))
    return results

main()
