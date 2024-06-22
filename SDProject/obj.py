class Question:
    def __init__(self):
        self.ID = 0
        self.Topic = ""
        self.Question = ""
        self.Answer = ""
        self.Hint = ""

    # A sample method
    def setValues(self, ID, Topic, Question, Answer, Hint):
        self.ID = ID
        self.Topic = Topic
        self.Question = Question
        self.Answer = Answer
        self.Hint = Hint
