# Movies Recommendation System Using Artificial Intelligence

## Overview

This project is a Movies Recommendation System that leverages artificial intelligence to suggest movies based on user input. It utilizes cosine similarity to compare movie descriptions and genres, providing personalized recommendations.

![App Screenshot](https://via.placeholder.com/800x400?text=App+Screenshot)

## Features

- **Movie Search**: Users can search for movies by title.
- **Recommendations**: Top 10 movie recommendations based on the selected movie.
- **Poster Fetching**: Retrieves movie posters from The Movie Database (TMDB) API.

## Technologies Used

- **Python**: Main programming language.
- **Streamlit**: Framework for building the web application.
- **Pandas**: Data manipulation and analysis.
- **Scikit-learn**: Used for cosine similarity calculations.
- **Requests**: For API calls to fetch movie data and posters.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/Movies-Recommendation-System.git
   cd Movies-Recommendation-System

   Install the required packages:
bash

Copy
pip install -r requirements.txt
Create a .env file and add your TMDB API key:
plaintext

Copy
TMDB_API_KEY=your_api_key_here
Usage
Run the Streamlit app:
bash

Copy
streamlit run application.py
Open your browser and navigate to http://localhost:8501 to view the app.
Type or select a movie to get recommendations.
Dataset
The dataset used in this project is the TMDB 5000 Movies Dataset, which includes various attributes of movies such as title, overview, and genres.

Contributing
Contributions are welcome! Please create a pull request for any improvements or features you would like to add.

License
This project is licensed under the MIT License - see the LICENSE file for details.

livecodeserver

Copy

### Instructions to Add the README

1. Go to your GitHub repository.
2. Click on "Add a README".
3. Copy and paste the above content into the README file.
4. Replace any placeholders (like `yourusername` and `your_api_key_here`) with your actual information.
5. Commit the changes.

This will provide a clear and informative overview of your project for anyone who visits your GitHub repository!
