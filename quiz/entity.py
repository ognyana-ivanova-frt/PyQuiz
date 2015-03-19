def _check_file_exist():
    """
    Checking file if exist
    :return: True|False
    """
    import os

    file_path = 'questions.txt'
    try:
        if os.stat(file_path).st_size > 0:  # check file size
            return True
        else:
            print "File is empty!"
            exit()
    except OSError:
        print 'No such file or directory: "{}"!'.format(file_path)
        exit()


def _get_user_input_values():
    """
    Asking user for configurations before the quiz starts
    """
    correct_count_questions_input = False
    correct_count_answers_input = False
    num_lines = sum(1 for line in open('questions.txt'))  # count of file lines
    Configurations.file_num_lines = num_lines
    while not correct_count_questions_input:
        try:
            user_count_questions = int(raw_input("Count questions: "))
            if user_count_questions <= Configurations.file_num_lines:  # check if user input value is correct
                correct_count_questions_input = True
                Configurations.count_questions = user_count_questions  # storing user input value in a property
                while not correct_count_answers_input:
                    try:
                        user_count_answers = int(raw_input("Count answers: "))
                        if 1 < user_count_answers <= _get_max_count_answers():  # check if user input value is correct
                            correct_count_answers_input = True
                            Configurations.count_answers = user_count_answers  # storing user input value in a property
                        else:
                            print "Min answers 2, Max answers {}".format(_get_max_count_answers())
                    except ValueError:
                        print "Oops!  That was no valid number.  Try again..."
            else:
                print "Max questions {}".format(Configurations.file_num_lines)
        except ValueError:
            print "Oops!  That was no valid number.  Try again..."


def _get_random_line_numbers():
    """
    Getting random line indexes from file
    """
    import random

    try:
        if Configurations.count_questions < Configurations.file_num_lines:  # check if user input value is correct
            random_line_numbers = random.sample(range(1, Configurations.file_num_lines),
                                                Configurations.count_questions)  # getting random line numbers from file
        else:
            random_line_numbers = range(1, Configurations.file_num_lines + 1)
            random.shuffle(random_line_numbers)

        Configurations.random_line_numbers = random_line_numbers  # storing random_line_numbers value in a property
    except ValueError:
        pass


def _get_max_count_answers():
    """
    Getting min length of answers for all questions
    :return int
    """
    max_count_answers = []
    with open("questions.txt", "r") as ins:
        for num, line in enumerate(ins, 1):
            line_elements = line.split("|")
            all_answers = line_elements[2:]  # getting answers from line
            max_count_answers.append(len(all_answers))

    return min(max_count_answers)


class Quiz(object):
    """
    Basic class quiz with all questions
    """

    def __init__(self):
        self._questions = []

    def load_quiz(self):
        """
        Basic method for loading a quiz
        """
        _check_file_exist()
        _get_user_input_values()
        _get_random_line_numbers()
        self._load_questions()

    def _load_questions(self):
        """
        Method for loading all questions
        """
        import random

        with open("questions.txt", "r") as ins:
            for num, line in enumerate(ins, 1):
                if num in Configurations.random_line_numbers:  # check if line number is in random lines
                    line_elements = line.split("|")
                    if len(line_elements) > 4:  # check if questions are correct
                        question_text = line_elements[0].replace("\\n", u"\n")  # \n means newline
                        question = Question(question_text)
                        correct_position = int(line_elements[1])

                        all_answers = line_elements[2:]  # getting answers from line

                        correct_answer_text = all_answers[correct_position]  # getting correct answers

                        all_answers = [answer.strip() for answer in all_answers if
                                       answer != correct_answer_text]  # strip answers without correct answer

                        all_answers = random.sample(all_answers,
                                                    Configurations.count_answers - 1)  # getting random answers

                        for answer_text in all_answers:
                            answer = Answer(answer_text, False)
                            question._add_answer(answer)  # set answer

                        correct_answer = Answer(correct_answer_text.strip(), True)
                        question._add_answer(correct_answer)  # set correct answer
                        question._shuffle_answers()
                        self._add_question(question)  # set question
                    else:
                        print 'Error in text file!'
                        exit()

    def get_questions(self):
        """
        :return: list[Question]
        """
        return self._questions

    def _add_question(self, question):
        """
        :param question: Question
        :return list[Questions]
        """
        self._questions.append(question)
        return self._questions


class Question(object):
    """
    Basic class question with all answers
    """
    def __init__(self, question_text):
        """
        :param question_text: string
        """
        self._question_text = question_text
        self._answers = []

    def _add_answer(self, answer):
        """
        :param answer: Answer
        :return list[Answer]
        """
        self._answers.append(answer)
        return self._answers

    def get_answers(self):
        """
        :return: list[Answer]
        """
        return self._answers

    def _shuffle_answers(self):
        """
        Shuffle answers
        """
        from random import shuffle

        shuffle(self._answers)

    def __str__(self):
        """
        :return: string
        """
        return self._question_text


class Answer(object):
    """
    Basic class answers
    """
    def __init__(self, answer_text, is_correct):
        """
        :param answer_text: string
        :param is_correct: boolean
        """
        self._answer_text = answer_text
        self.is_correct = is_correct

    def __str__(self):
        """
        :return string
        """
        return '{} {}'.format(self._answer_text, str(self.is_correct))


class Configurations(object):
    """
    Static class with application configurations
    """
    count_questions = 0
    count_answers = 0
    max_count_answers = 0
    random_line_numbers = 0
    file_num_lines = 0

