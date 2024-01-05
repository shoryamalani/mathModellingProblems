m_probabilities = [9,18,21,14,12,20]
m_total = sum(m_probabilities)
possibilties = []
# find the probability of picking 3 having all unique numbers without replacement
total_probability = 0
for a in range(0,6):
    for b in range(0,6):
        for c in range(0,6):
            if a != b and a != c and b != c and set([a,b,c]) not in possibilties:
                total_probability += (m_probabilities[a]*m_probabilities[b]*m_probabilities[c])/(m_total*(m_total-1)*(m_total-2))
                possibilties.append(set([a,b,c]))
                
print(total_probability)

