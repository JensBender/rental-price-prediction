<!-- anchor tag for back-to-top links -->
<a name="readme-top"></a>


## Table of Contents
<ol>
  <li>
    <a href="#about-the-project">About The Project</a>
    <ul>
      <li><a href="#summary">Summary</a></li>
      <li><a href="#built-with">Built With</a></li>
    </ul>
  </li>
  <li>
    <a href="#motivation">Motivation</a>
  </li>
  <li>
    <a href="#data">Data</a>
  </li>
  <li>
    <a href="#model-building">Model Building</a>
  </li>
  <li>
    <a href="#getting-started">Getting Started</a>
    <ul>
      <li><a href="#prerequisites-for-data-collection-and-preprocessing">Prerequisites for Data Collection and Preprocessing</a></li>
      <li><a href="#prerequisites-for-model-training">Prerequisites for Model Training</a></li>
    </ul>
  </li>
</ol>


<!-- ABOUT THE PROJECT -->
## About The Project

### Summary
+ Motivation: Utilize machine learning to predict rental prices. 
+ Data collection: Scraped 1680 property listings from an online property portal in Singapore.
+ Exploratory data analysis: Utilized a word cloud to inform feature extraction from property agent comments. Visualized property locations on an interactive map of Singapore using Python's Folium library. Explored descriptive statistics, distributions and correlations. 
+ Data preprocessing: Removed duplicates and handled missing values.
  + Data enrichment: Filled in missing addresses based on property names using the Google Maps API.
  + Feature engineering: Utilized the Google Maps API to obtain (a) latitude and longitude based on the address, (b) distance to the central business district, (c) distance to the closest school, and (d) average rating of nearby restaurants.
  + Feature extraction: Extracted property type, furnishing, built year, distance to MRT and other features from the property descriptions.
  + Handling outliers: Removing rental price outliers based on 1.5 interquartile ranges improved model performance compared with removing outliers based on 3 standard deviations or not removing outliers.
+ Model training: 
  + Baseline model performance: XGBoost (RMSE: 1151) and random forest (RMSE: 1110) demonstrated superior performance compared to linear regression (RMSE: 1369), support vector machine (RMSE: 2087), and neural network (RMSE: 1370).
  + Hyperparameter tuning: Performed a grid search of XGBoost and random forest. 
  + Model selection: The best performing model was an XGBoost model with RMSE 995, MAPE 0.13 and R-squared 0.9 on the test data.

### Built With
* [![Python][Python-badge]][Python-url]
* [![NumPy][NumPy-badge]][NumPy-url]
* [![Pandas][Pandas-badge]][Pandas-url]
* [![Matplotlib][Matplotlib-badge]][Matplotlib-url]
* [![scikit-learn][scikit-learn-badge]][scikit-learn-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MOTIVATION -->
## Motivation
+ Problem: The property market in Singapore is one of the most expensive in the world. Finding a good deal is hard and determining whether a property listing is a good deal or overpriced is difficult.
+ Project goal: Utilize the power of machine learning to help people in their search of rental properties by developing a tool that estimates rental prices and helps to determine whether a property listing is overpriced or a good deal. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- DATA COLLECTION -->
## Data Collection
+ Scraped 5360 property listings (1680 after removing duplicates) from an online property portal in Singapore using cloudscraper and Beautiful Soup.
+ Extracted the following information from the property listings: Property name, price, address, size, bedrooms, bathrooms, property type, furnishing, build year, distance to MRT, and agent description.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites for Data Collection and Preprocessing
This is a list of the Python packages you need.  
+ Data collection
  + Cloudscraper
  + Beautiful Soup
  + lxml
  + Pandas
+ Data preprocessing
  + Numpy
  + Pandas
  + Matplotlib
  + Seaborn
  + Requests
  + Dotenv

### Prerequisites for Model Training
This is a list of the Python packages you need.  
+ Model training
  + Numpy
  + Pandas
  + Matplotlib
  + Scikit-learn
  + XGBoost
  + Pickle


<!-- MARKDOWN LINKS -->
[Python-badge]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[NumPy-badge]: https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white
[NumPy-url]: https://numpy.org/
[Pandas-badge]: https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white
[Pandas-url]: https://pandas.pydata.org/
[Matplotlib-badge]: https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black
[Matplotlib-url]: https://matplotlib.org/
[scikit-learn-badge]: https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white
[scikit-learn-url]: https://scikit-learn.org/stable/
