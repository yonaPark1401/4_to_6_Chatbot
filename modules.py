from navec import Navec
import numpy as np
from numpy.linalg import norm


def angle(v1, v2):
  return np.dot(v1, v2)/(norm(v1)*norm(v2))

def vectorize_text(text):
  text = text.split(' ')
  text_length = len(text)
  get_vecs = [navec[text[i]] for i in range(3)]
  text_vector = sum(get_vecs) / text_length
  return text_vector


# ------------------------------------------------------------------------------------------------------------
path = 'navec_hudlit_v1_12B_500K_300d_100q.tar'
navec = Navec.load(path)
google_search_command = [
  'посмотри в интернете',
  'поищи в гугле',
  'найди в инете'
]
threshold = 0.75
google_search_vector = sum([vectorize_text(google_search_command[i])
                            for i in range(len(google_search_command))]) / len(google_search_command)

def compare_vecs(text):
  try:
    text_vec = vectorize_text(text)
    cosine_distance = angle(google_search_vector, text_vec)
    response = True if cosine_distance > threshold else False
  except:
    response = False
  return response








