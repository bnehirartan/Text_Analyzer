import string
import re
from collections import Counter
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import nltk

#stopwords: A collection of stop words for various languages. Stop words are common words like "the", "is", "in", etc., which are usually filtered out during text processing.
#wordnet: A lexical database for the English language, which groups English words into sets of synonyms called synsets, provides short definitions and usage examples, and records a number of relations among these synonym sets or their members.
#punkt: A pre-trained model for tokenizing text into sentences.
#averaged_perceptron_tagger: A part-of-speech tagger model that assigns parts of speech to each word in a text.


nltk.download('stopwords')
nltk.download('wordnet')

class TextAnalyzer:
    def __init__(self, text):
        self.original_text = text
        self.fmtText = self._format_text(text)
        self.word_freq = self._compute_word_frequency()

    def _format_text(self, text):
        text = text.lower() #lowercase
        text = text.translate(str.maketrans('', '', string.punctuation)) #removing punctuation
        text = re.sub(r'\d+', '', text) #removing numbers
        text = ' '.join(text.split()) #removing extra space
        return text


    def _remove_stopwords(self, words):
        stop_words = set(stopwords.words('english')) #stopwords.words('english'): This function from the nltk.corpus module provides a list of stop words in English.
        filtered_words = [word for word in words if word not in stop_words] #creates a new list of words, excluding those that are stop words
        return filtered_words

#Stemming is a process that removes suffixes from words, which can help in reducing word variants to a common base form.
    def _stem_words(self, words):
        ps = PorterStemmer() # a stemming algorithm provided by the nltk.stem module
        stemmed_words = [ps.stem(word) for word in words] #applies the stem method to each word in the list, produces a list of stemmed words
        return stemmed_words

#lemmatization considers the context and converts words to their meaningful base forms.
    def _lemmatize_words(self, words):
        lemmatizer = WordNetLemmatizer() # a lemmatizer provided by the nltk.stem module that uses the WordNet lexical database
        lemmatized_words = [lemmatizer.lemmatize(word) for word in words] #applies the lemmatize method to each word in the list, produces a list of lemmatized words.
        return lemmatized_words

    def _compute_word_frequency(self):
        words = self.fmtText.split()
        words = self._remove_stopwords(words)
        words = self._lemmatize_words(words)
        word_freq = Counter(words)
        return word_freq

    def freqAll(self):
        return self.word_freq

    def freqOf(self, word):
        word = word.lower()
        word = re.sub(r'\d+', '', word)
        word = word.translate(str.maketrans('', '', string.punctuation))
        word = ' '.join(word.split())
        word = self._lemmatize_words([word])[0]
        return self.word_freq.get(word, 0)

    def visualize_word_frequency(self, top_n=10):
        most_common_words = self.word_freq.most_common(top_n)
        words, counts = zip(*most_common_words)

        plt.figure(figsize=(10, 5))
        plt.bar(words, counts, color='blue')
        plt.xlabel('Words')
        plt.ylabel('Frequency')
        plt.title('Top {} Most Frequent Words'.format(top_n))
        plt.show()

#sample
if __name__ == "__main__":
    givenstring = "In a distant, but not so unrealistic, future, humanity is on the brink of extinction. Climate change, resource depletion, and overpopulation have taken their toll. However, amid the chaos, hope emerges. Scientists discover a new planet, capable of sustaining human life. The journey to this new world is perilous, filled with unknown challenges and dangers. Yet, the promise of a fresh start drives humanity forward."
    
    analyzed = TextAnalyzer(givenstring)
    print("Formatted Text:", analyzed.fmtText)
    
    freqMap = analyzed.freqAll()
    print("Frequency of all unique words:", freqMap)
    
    word = "lorem"
    frequency = analyzed.freqOf(word)
    print(f"The word '{word}' appears {frequency} times.")
    
    analyzed.visualize_word_frequency(top_n=5) #TopN