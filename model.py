import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

dosha = {
    'Vata': ['sweet', 'sour', 'salty'],
    'Kapha': ['astringent', 'bitter', 'pungent'],
    'Pitta': ['sweet', 'bitter', 'astringent'],
    '': ['sweet', 'sour', 'salty', 'astringent', 'bitter', 'pungent']

}

data = pd.read_csv('indian_food.csv')
ingredient_matrix = pd.get_dummies(data['ingredients'].str.split(
    ",").apply(pd.Series).stack()).groupby(level=0).sum()
similarity = cosine_similarity(ingredient_matrix)


def get_recommendations(title, dosh=None, top_n=5):
    # Find the index of the movie with the given title
    idx = data[data['name'] == title].index[0]

    # Get the cosine similarity scores for the dish
    similarity_scores = list(enumerate(similarity[idx]))

    # Sort the similarity scores in descending order
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1] if (
        data['flavor_profile'].iloc[x[0]] in dosha[dosh]) else 0, reverse=True)
    # print(similarity_scores[1:6])
    # Get the top_n dish indices
    food_indices = [i[0] for i in similarity_scores[1:top_n+1]]
    # Return the top_n most similar foods
    return data['name'].iloc[food_indices]
