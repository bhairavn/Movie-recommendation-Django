import pandas as pd
import numpy as np
from .colab_filter import recommend

def closest(lst):
      
  combined = np.zeros((9623889, 4))
  result_df = pd.read_csv("Movierecommendation/closest_users.csv")
  combined = result_df.to_numpy()
  error = 1000
  closest_id = 5
  user_start = 0
  user_start = 0

  for user_id in range(10000):

    no_of_movies = 0
    user_end = user_start
    for x in range (user_start, 9623889):
      if (combined[x, 1]==user_id):

        no_of_movies+=1
      else:
        break
    user_end += no_of_movies
    iter_error = 10*len(lst)
    for x in range(user_start, user_end):
      #if user_start==0:
      #print(combined[x,:])
      for tup in lst:
        if combined[x,2]==tup[0]:
          iter_error= iter_error-10+ abs(tup[1]-combined[x,4])

    #if iter_error<10:
    #  print(iter_error)
    if iter_error<= error:

      closest_id = user_id
      error = iter_error

      #print(closest_id)
    user_start = user_end

  return closest_id

# tuples in the form of movieid, rating
# lst = [(521,3),(241,3),(1311,4)]
# temp_id = closest(lst)

# print(recommend(temp_id))
