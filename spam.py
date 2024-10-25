import sys,dataset, math
spam_words =dataset.word_countt['spam']
ham_words =dataset.word_countt['ham']

def preprocess_email(email):
    # Lowercase the email and remove punctuation
    email = email.lower()
    punctuation = "|\\><~@#$%^&*_.,!?\"'()[]{};:"
    
    for char in punctuation:
        email = email.replace(char, "")
    return email.split()

def spam_detector(email):
    # Preprocess both subject and body
    words = preprocess_email(email)

    #count words in spam and ham 
    spam_count=sum(spam_words.values())
    ham_count=sum(ham_words.values())
    
    # Initialize log probabilities for spam and ham
    prob_spam = 0
    prob_ham = 0

    # Calculate the log probabilities for each word in the email
    for word in words[1:]:
        # Get the count of the word in spam and ham datasets, get handles key errors
        spam_word_count = spam_words.get(word, 0)
        ham_word_count = ham_words.get(word, 0)

        # Calculate the probabilities with Laplace smoothing
        prob_word_given_spam = (spam_word_count + 1) / (spam_count + len(spam_words))
        prob_word_given_ham = (ham_word_count + 1) / (ham_count + len(ham_words))

        # Update log probabilities
        prob_spam += math.log(prob_word_given_spam)
        prob_ham += math.log(prob_word_given_ham)
    
    # Calculate prior probabilities
    prior_prob_spam = spam_count / (spam_count + ham_count)
    prior_prob_ham = ham_count / (spam_count + ham_count)

    # Final log probabilities by adding the prior probabilities
    prob_spam += math.log(prior_prob_spam)
    prob_ham +=math.log(prior_prob_ham)

    # Classify the email based on the log probabilities
    if  prob_spam > prob_ham:
        return 'spam'
    else:
        return 'notspam'

def main():
    if  len(sys.argv)==2:
        file=sys.argv[1]
        with open(file, 'r', errors='ignore') as f:
            contents = f.read().lower()
        print(spam_detector(contents))
    else:
        print("Please enter file name before running code")
if __name__ == "__main__":
    main()