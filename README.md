# Visualizing Geospatial Data with H3 Hexagons



## Introduction

This is a h3 visualization project I conducted during my tenure as a Data Scientist intern. The aim of this project is to represent the population, income, and number of charging stations in Taiwan in a 3D hexagonal format on a map of Taiwan, in order to generate more ideas for future charging station deployment. The conversion of h3 hexagons into 3D format primarily utilized the Python third-party package, Ellipse.

## Data Source

1.	Taiwan Population and income data on the socio-economic data service platform. [Platform Link](https://segis.moi.gov.tw/STAT/Web/Platform/QueryInterface/STAT_QueryTopProduct.aspx )
2.	Charging station : The data on charging station locations across Taiwan is confidential as it originates from a company source.


## 3D Visualization Demo Link

[Population](https://app.ellipsis-drive.com/view?pathId=94a96cbb-fa8f-4f2a-85d3-00079affb103&state=249c0b16-5854-44d9-95c4-ddf08b69df48)

[Income](https://app.ellipsis-drive.com/view?pathId=94a96cbb-fa8f-4f2a-85d3-00079affb103&state=fe41a0c2-a947-4466-8477-1b3d3253b8d9)

[Charge Sation](https://app.ellipsis-drive.com/view?pathId=94a96cbb-fa8f-4f2a-85d3-00079affb103&state=f37270a1-157f-4605-a9ef-88dc8fd57015)


## Tools Used

- **Python**


## Project Structure

```plaintext
h3_visualization/
├── code/                       # Folder containing Python code files.
│   ├── cal_hexagons.py         # .py file used by h3_visualization.ipynb
│   └── h3_visualization.ipynb
├── data/                       # Folder containing geographical data of Taiwan.
│   ├── TaiwanTownMap           # This folder contains geographical data of Taiwan, organized by town.
│   ├── TaiwanVillageMap        # This folder contains geographical data of Taiwan, organized by village.
│   └── Village                 # This folder contains data on the population and income of Taiwan, organized by village.

├── report/                     # Folder containing the project report details in .pptx format.
│   └── h3_visualization_project.pptx
│
└── README.md                   # This file.
```

## Contact Information

For any further questions or collaboration opportunities, please reach out to me at:
- Email: [yguo8395@gmail.com](mailto:yguo8395@gmail.com)
- LinkedIn: [Iris Kuo](https://www.linkedin.com/in/yi-hsuan-kuo-835b00268/)
- GitHub: [Iris Kuo](https://github.com/Iris910531)
