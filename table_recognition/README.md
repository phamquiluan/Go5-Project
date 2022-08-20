# Table Structure Recognition
Table Structure Recognition (TSR) problem aims to recognize the structure of a table and transform the unstructured tables into a structured and machine-readable format so that the tabular data can be further analysed by the down-stream tasks, such as semantic modeling and information retrieval [(1)](https://arxiv.org/abs/2203.03819).
Chosen along the product, we are handling TSR problem using [`table-transformer(DETR)`](https://github.com/microsoft/table-transformer).

![image](https://user-images.githubusercontent.com/86721208/185638706-62903496-ff20-4bfc-bf8a-e98bde5b2059.png)

---
## I. Installation

1. Setup the environment from `\table_recognition\requirements.txt` as follows:
    ```
    pip install -r requirements.txt
    ```
2. The checkpoint in use can be found here: [pubtables1m_structure_detr_r18.pth](https://pubtables1m.blob.core.windows.net/model/pubtables1m_structure_detr_r18.pth). </br>
   Download the checkpoint and put it in folder `checkpoints` in the root of dir `\table_recognition` (create one if none).
3. Clone the repository [table-transformer](https://github.com/minhngt62/table-transformer.git) into the root of dir `\table_recognition`
4. To re-produce the evaluation in `\table_recognition\table_recognition.ipynb`, download the specific structure dataset from [PubTables-1M](https://msropendata.com/datasets/505fcbe3-1383-42b1-913a-f651b8b712d3), and put it in folder `data` in the root of dir `table-transformer` (create one if none). </br>
   Notice that this dataset is quite heavy with limit download bandwidth (2 hours of downloading estimated).

For full instruction of usage and installation, please then follow: `\table_recognition\table_recognition.ipynb`

---
## II. Issues & Resolve
### Physical overlapping of table's hierarchical structure
Our aim of TSR task is to extract certain cells, not any hierarchical structures. The problem here is that `table-transformer(DETR)` returns a hierarchical structure of table of six object classes: table, table column, table row, table column header, table projected row header, and table spanning cell. The seventh class - grid cell, which we want to extract, can be formed from the intersection of each pair of table column and table row objects [(2)](https://arxiv.org/abs/2110.00061). It arises an issue that objects of different classes may overlap physically each other, hindering efforts to extract a single, exact cell for each functional area of the table using bounding boxes.

<p align="center">
  <img src="https://user-images.githubusercontent.com/86721208/185650042-4873417b-ee04-4026-b595-ade1d1d8d044.jpg">
</p>

Therefore, a temporary measure has been introduced to reduce the overlapping: Remove the grid cells that intersect largely a certain spanning cell, aligned with functional analysis bounding boxes deletion.
- The hyperparameter `oversegment` in class `TableRecognizer`: A grid cell is marked deleted if the intersection area of its with any spanning cells is larger than a constant ratio, compared to its own area. We call that ratio as `intersection_ratio` which can be easily computed by: `intersect_area / grid_cell_area`.
    - `oversegment = True`: Overlapping cells will not be filtered.
    - `oversegment = x` (x in [0, 1]): Overlapping cells will be filtered if its intersection ratio passes x.

### Tight tables' bounding box
Table detection (TD) task frequently returns greatly tight bounding boxes which eliminates the surrounding area of table. Observed, it, by somehow, often squeezes or displaces the grid cells' bounding box from the grouth truth. A suggested schema is to extract cropped table by adding an offset to each coordinated extracted from TD, which surprisingly acquires a greatly postitive observable result against the issue of tightness.

<p align="center">
  <img src="https://user-images.githubusercontent.com/86721208/185764463-f38424d6-a03a-4873-8dd2-83d70e4dc14e.png">
</p>

- The hyperparameter `offset` in class `TableRecognizer`: With `offset=x`, the algorithm will leave an offset area, whose edges are more x pixels, surrounding the cropped table.



