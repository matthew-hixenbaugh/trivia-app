from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"
QUESTION_FONT = ('Arial', 20, 'italic')
SCORE_FONT = ('Arial', 16)
CORRECT_COLOR = "#98FB98"
INCORRECT_COLOR = "#FF5733"


class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain

        self.window = Tk()
        self.window.title("20 Questions")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        true_button_image = PhotoImage(file='./images/true.png')
        false_button_image = PhotoImage(file='./images/false.png')

        self.true_button = Button(master=self.window, image=true_button_image, highlightthickness=0,
                                  command=lambda: self.check_answer_button(True))
        self.false_button = Button(master=self.window, image=false_button_image, highlightthickness=0,
                                   command=lambda: self.check_answer_button(False))

        self.score_label = Label(master=self.window, text='Score = 0', font=SCORE_FONT, fg='white', bg=THEME_COLOR)

        self.question_box = Canvas(master=self.window, width=300, height=250, bg='white', highlightthickness=0)
        self.question_text = self.question_box.create_text(150, 125, text=self.quiz.next_question(), fill=THEME_COLOR,
                                                           font=QUESTION_FONT, width=280)

        self.score_label.grid(row=0, column=1)
        self.question_box.grid(row=1, column=0, columnspan=2, pady=50)
        self.true_button.grid(row=2, column=0)
        self.false_button.grid(row=2, column=1)

        self.window.mainloop()

    def get_next_question(self):
        if self.quiz.still_has_questions():
            self.enable_buttons()
            self.question_box.configure(bg='white')
            question_text = self.quiz.next_question()
            self.question_box.itemconfig(self.question_text, text=question_text)
        else:
            self.create_end_screen()

    def check_answer_button(self, answer: bool):
        is_correct = self.quiz.check_answer(answer)
        self.update_ui(is_correct)

    def update_ui(self, is_correct: bool):
        self.disable_buttons()

        self.score_label.config(text=f"Score = {self.quiz.score}")
        if is_correct:
            self.question_box.configure(bg=CORRECT_COLOR)
        else:
            self.question_box.configure(bg=INCORRECT_COLOR)

        self.window.after(1000, self.get_next_question)

    def create_end_screen(self):
        if self.quiz.has_passed():
            self.question_box.configure(bg=CORRECT_COLOR)
            self.question_box.itemconfig(self.question_text,
                                         text=f"Congratulations! "
                                              f"You answered {self.quiz.score}/{len(self.quiz.question_list)} "
                                              f"questions correctly!")
        else:
            self.question_box.configure(bg=INCORRECT_COLOR)
            self.question_box.itemconfig(self.question_text,
                                         text=f"You answered {self.quiz.score}/{len(self.quiz.question_list)} "
                                              f"questions correctly.")

    def enable_buttons(self):
        self.true_button.configure(state="normal")
        self.false_button.configure(state="normal")

    def disable_buttons(self):
        self.true_button.configure(state="disabled")
        self.false_button.configure(state="disabled")
