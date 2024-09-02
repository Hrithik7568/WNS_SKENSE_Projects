from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap
from textblob import TextBlob, Word
import random
import time
import nltk
nltk.download('movie_reviews')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('brown')
nltk.download('stopwords')



#Initializes a Flask application instance. Integrates the Bootstrap library for styling the web application.

app=Flask(__name__)
Bootstrap(app)

# Defines the route for the homepage (root URL) of the web application.
# The function associated with this route. When a user accesses the root URL (/), this function is executed.

@app.route('/')
def index():
    return render_template('index.html')

# Defines the route for the /analyse URL, which handles POST requests from the client.

@app.route('/analyse', methods=['POST'])
def analyse():
    from textblob import blob
    start=time.time()
    if request.method=='POST':
        rawtext=request.form['rawtext']
        blob= TextBlob(rawtext)
        received_text=blob
	    
# Polarity - attribute of text blob library quantifies positivity or negativity.
# Subjectivity - attribute measures factual or aspect of text.
	    
        blob_sentiment,blob_subjectivity=blob.sentiment.polarity, blob.sentiment.subjectivity
        number_of_tokens=len(list(blob.words))
        nouns=list()

# Analyze it for sentiment, tokenize it, identify nouns, and perform random shuffling and pluralization of the nouns.
	    
        for word, tag in blob.tags:
            if tag=='NN':
                nouns.append(word.lemmatize())
                len_of_words=len(nouns)
                rand_words=random.sample(nouns, len(nouns))
                final_word=list()
                for item in rand_words:
                    word=Word(item).pluralize()
                    final_word.append(word)
                    summary= final_word
                    end=time.time()
                    final_time=end-start

    return render_template('index.html',received_text = received_text,number_of_tokens=number_of_tokens,blob_sentiment=blob_sentiment,blob_subjectivity=blob_subjectivity,summary=summary,final_time=final_time)




# Ensures that the Flask app runs only if the script is executed directly (and not imported as a module

if __name__ == '__main__':
	app.run(debug=True)
