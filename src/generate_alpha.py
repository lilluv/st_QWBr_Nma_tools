import random

# class Alpha_Generator():
#     def __init__(self):
#         pass

#     def generator(self, list_alpha, field_neutralization = 'industry'):
#         n_alpha = len(list_alpha)
#         w_alpha = random.sample(range(1, 50), n_alpha)
#         w_alpha = w_alpha/sum(w_alpha)
        
#         for idx, alpha in enumerate(list_alpha):
#             alpha = "scale(group_neutralize({0}), {1}) * {2}".format(alpha, field_neutralization, w_alpha[idx])
#         f_alpha = ','.join(list_alpha)
#         return "add({0})".format(f_alpha)

def generator(list_alpha, field_neutralization = 'industry'):
    n_alpha = len(list_alpha)
    random_weight = random.sample(range(1, 10), n_alpha)
    # w_alpha = [x/sum(random_weight) for x in random_weight ]
    w_alpha = random_weight
    
    list_processed_alpha = []
    for idx, alpha in enumerate(list_alpha):
        # alpha = "scale(group_neutralize({0}, {1})) * {2}".format(alpha, field_neutralization, w_alpha[idx])
        alpha = "scale(group_neutralize({0}, {1}))".format(alpha, field_neutralization)
        list_processed_alpha.append(alpha)

    f_alpha = ','.join(list_processed_alpha)
    print(f_alpha)
    return "add({0})".format(f_alpha)

