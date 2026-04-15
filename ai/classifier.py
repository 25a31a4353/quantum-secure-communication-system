from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

class MessageClassifier:
    def __init__(self):
        # A simple dummy dataset to train the classifier
        self.texts = [
            "Hello, how are you?", 
            "What's the plan for today?", 
            "Can we meet at 5 PM?", 
            "Are we still on for lunch?", 
            "Sounds good, see you then.", 
            "I will call you later.",
            "Congratulations! You've won a $1000 prize. Click here.", 
            "Buy cheap pills online now!", 
            "Earn money fast from home.", 
            "You have been selected for a free gift.", 
            "Claim your inheritance now.",
            "My social security number is 123-456-7890", 
            "Here is the password for the server: admin123", 
            "Please transfer the funds to account number 987654321", 
            "Send me the secret project files secretly", 
            "The launch codes are 0000"
        ]
        self.labels = [
            "Safe", "Safe", "Safe", "Safe", "Safe", "Safe",
            "Spam", "Spam", "Spam", "Spam", "Spam",
            "Sensitive", "Sensitive", "Sensitive", "Sensitive", "Sensitive"
        ]
        
        self.vectorizer = TfidfVectorizer()
        self.classifier = MultinomialNB()
        
        # Train immediately upon initialization
        if self.texts:
            X = self.vectorizer.fit_transform(self.texts)
            self.classifier.fit(X, self.labels)
        
    def classify(self, message):
        if not message.strip():
            return "Safe"
            
        X_test = self.vectorizer.transform([message])
        prediction = self.classifier.predict(X_test)[0]
        
        # Add basic rule-based detection for critical info which naive bayes might miss on tiny dataset
        message_lower = message.lower()
        if any(word in message_lower for word in ["password", "secret", "account", "social security", "credit card"]):
            return "Sensitive"
            
        return prediction

# Create a singleton instance 
classifier_instance = MessageClassifier()

def get_message_classification(message):
    return classifier_instance.classify(message)
