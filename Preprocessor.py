# Creating a function to measure distance between users
def col_dist(u1,u2):
    return pow(sum(pow(u1[i]-u2[i],2) for i in range(len(u1))),0.5)

def distance_from_remaining_users(user,user_matrix):
    distances = []
    for i in range(len(user_matrix)):
        dist = col_dist(user,user_matrix[i])
        distances.append(dist)
    return distances

# #  Finding the top 10 songs from above list of songs
# def top_n_songs(nearest_users,df,n):
#     temp = df.iloc[nearest_users]
#     dict1 = temp.max().to_dict()
# # converting every key value pair into tuple and swaping them for sorting purpose end result is s list of songs and number of times heared tuple
#     sorted_dict = sorted(dict1.items(),key = lambda keyvalue:(keyvalue[1],keyvalue[0]),reverse = True)[:n]
#     return [x[0] for x in sorted_dict]

def get_keys_by_value(dictionary, target_value):
    return [key for key, value in dictionary.items() if value == target_value]