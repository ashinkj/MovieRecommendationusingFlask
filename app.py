from turtle import title
import flask
import difflib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = flask.Flask(__name__, template_folder='templates')

df2 = pd.read_csv('./model/tmdb.csv')

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df2['soup'])

cosine_sim2 = cosine_similarity(count_matrix, count_matrix)


df2 = df2.reset_index()
indices = pd.Series(df2.index, index=df2['title'])
##print(indices.head())
all_titles = [df2['title'][i] for i in range(len(df2['title']))]

def get_recommendations(title):
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    tit = df2['title'].iloc[movie_indices]
    dat = df2['release_date'].iloc[movie_indices]
    genr= df2['genres'].iloc[movie_indices]
    #lnk= df2['homepage'].iloc[movie_indices]
    return_df = pd.DataFrame(columns=['Title','Year','genres','homepage'])
    return_df['Title'] = tit
    return_df['Year'] = dat
    return_df['genres'] = genr
    #return_df['homepage'] = lnk
    return return_df

# Set up the main route

@app.route('/', methods=['GET', 'POST'])

def main():
    if flask.request.method == 'GET':
        return(flask.render_template('index.html'))
    
            
    if flask.request.method == 'POST':
        m_name = flask.request.form['movie_name']
        m_name = m_name.title()
        df2.homepage = df2.homepage.fillna(' ')
        #check = difflib.get_close_matches(m_name,all_titles,cutout=0.50,n=1)
        if m_name not in all_titles:
            return(flask.render_template('negative.html',name=m_name))
        else:
            result_final = get_recommendations(m_name)
            names = []
            dates = []
            genres = []
            movie_link=(df2.iloc[indices[m_name]]['homepage'])
            movie_details=(df2.iloc[indices[m_name]]['overview'])
            for i in range(len(result_final)):
                names.append(result_final.iloc[i][0])
                dates.append(result_final.iloc[i][1])
                genres.append(result_final.iloc[i][2])
            return flask.render_template('positive.html',movie_names=names,movie_date=dates,search_name=m_name,movie_genre=genres,link1=movie_link,details1=movie_details)        

if __name__ == '__main__':
    app.run()  