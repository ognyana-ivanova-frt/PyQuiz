from quiz.entity import Quiz


class QuizController(object):
    """
    Main quiz controller
    """

    def __init__(self):
        self._quiz = Quiz()
        self._quiz.load_quiz()
        self._user_input = ''
        self._answers_letter_map = {}
        self._count_correct_answers = 0
        self._count_questions = 0

    def ask_question(self):
        """
        Starting quiz
        """
        import string

        letters_list = list(string.ascii_uppercase)
        questions = self._quiz.get_questions()
        self._count_questions = len(questions)
        i = 1
        for question in questions:
            print '{}. {}'.format(i, question)  # format output question
            question_answers = question.get_answers()
            i += 1
            for j, answer in enumerate(question_answers):
                self._answers_letter_map[letters_list[j]] = answer
                print '{}) {}'.format(letters_list[j], answer._answer_text)  # format output answer

            self.process_user_input(question)

        print "You have {}/{} correct answers".format(self._count_correct_answers,
                                                      self._count_questions)  # end of quiz


    def request_user_input(self):
        """
        Requesting user input and storing it in a property
        """
        self._user_input = raw_input("Please enter an answer: ")
        self._user_input = self._user_input.upper().strip()

    def process_user_input(self, question):
        """
        Processing while given answer is correct
        :param question: Question
        """
        correct_user_input = False
        while not correct_user_input:
            self.request_user_input()
            if self._user_input in self._answers_letter_map:
                correct_user_input = True
                result = self.check_question(question)
                if result:
                    print "Correct!"
                    self._count_correct_answers += 1
                else:
                    print "Wrong!!!"
            else:
                print "Oops!  That was no valid answer.  Try again..."

    def check_question(self, question):
        """
        Checking answer for given question
        :param question: Question
        :return: True|False
        """
        answer = self._answers_letter_map[self._user_input]
        return answer.is_correct
