import tkinter as tk

pos = -1

def log():
	global pos
	pos = -1
	userdata = []
	pow = []
	MOD = int(1e9) + 9277


	def prep_hash():
		BASE = 256
		MAX = 320

		pow.append(1)
		for i in range(1, MAX):
			pow.append(pow[i - 1] * BASE % MOD)

	def trans_list(data):
		for line in data:
			number = ""
			tmp = []
			for i in range(0, len(line)):
				if line[i] == '\n':
					break
				if line[i] == ' ':
					tmp.append(number)
					number = ""
				else: 
					number += line[i]
			userdata.append(tmp)

	def trans_str():
		info = str("")
		for i in userdata:
			tmp = str("")
			for j in i:
				tmp += str(j) + ' '
			info += tmp
			info += '\n'
		file = open("./asset/data/userdata.txt", "w")
		file.write(info)
		file.close()

	try:
		# file = open("./asset/data/userdata.txt", "a")
		# file.close()
		file = open("./asset/data/userdata.txt", "r+")
		data = file.readlines()
		trans_list(data)
		file.close()
	except FileNotFoundError:
		print("File not Found.")
		exit()	

	# --------------------------------------------------------------------------------

	WINDOW_WIDTH = 1200
	WINDOW_HEIGHT = 675

	root = tk.Tk()

	root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{int(root.winfo_screenwidth()/2 - WINDOW_WIDTH/2)}+{int(root.winfo_screenheight()/2 - WINDOW_HEIGHT/2)}")
	root.resizable(False, False)
	root.iconbitmap("./asset/image/logo.ico")
	root.title("Life is lie")

	login_bg = tk.PhotoImage(file="./asset/image/login_bg.png")
	signup_bg = tk.PhotoImage(file="./asset/image/signup_bg.png")
	reset_password_bg = tk.PhotoImage(file="./asset/image/reset_password_bg.png")

	show = tk.PhotoImage(file="./asset/image/show.png")
	hide = tk.PhotoImage(file="./asset/image/hide.png")
	go_back = tk.PhotoImage(file="./asset/image/go_back.png")
	go_to = tk.PhotoImage(file="./asset/image/go_to.png")

	required_username = tk.PhotoImage(file="./asset/error/required_username.png")
	find_username = tk.PhotoImage(file="./asset/error/find_username.png")
	begin_username = tk.PhotoImage(file="./asset/error/begin_username.png")
	invalid_username = tk.PhotoImage(file="./asset/error/invalid_username.png")
	username_limit = tk.PhotoImage(file="./asset/error/username_limit.png")
	username_existed = tk.PhotoImage(file="./asset/error/username_existed.png")

	required_password_login = tk.PhotoImage(file="./asset/error/required_password_login.png")
	required_password = tk.PhotoImage(file="./asset/error/required_password.png")
	invalid_password = tk.PhotoImage(file="./asset/error/invalid_password.png")
	password_limit = tk.PhotoImage(file="./asset/error/password_limit.png")
	match_password = tk.PhotoImage(file="./asset/error/match_password.png")

	required_repassword = tk.PhotoImage(file="./asset/error/required_repassword.png")
	match_repassword = tk.PhotoImage(file="./asset/error/match_repassword.png")

	required_email = tk.PhotoImage(file="./asset/error/required_email.png")
	invalid_email = tk.PhotoImage(file="./asset/error/invalid_email.png")
	email_existed = tk.PhotoImage(file="./asset/error/email_existed.png")
	find_email = tk.PhotoImage(file="./asset/error/find_email.png")

	# --------------------------------------------------------------------------------

	def delete_errors(*error):
		for i in error:
			i.place_forget()

	def reset_state(*state):
		for i in state:
			i.config(image=hide)

	def change_frame(src, des, *text):
		for i in text:
			i.delete(0, "end")
		src.forget()
		des.pack(expand=True, fill="both")

	def show_password(state, entry):
		state.config(image=show)
		entry.config(show="")
		state.config(command=lambda: hide_password(state, entry))

	def hide_password(state, entry):
		state.config(image=hide)
		entry.config(show="•")
		state.config(command=lambda: show_password(state, entry))

	def invalid_letter(letter):
		return not(
				(letter >= '0' and letter <= '9')
				or (letter >= 'A' and letter <= 'Z')
				or (letter >= 'a' and letter <= 'z'))

	def pos_user(email):
		l = int(0)
		r = len(userdata) - 1
		mid = int((r + l) / 2)
		
		if (r < 0): 
			return -1

		while (True):
			if l + 1 >= r:
				if int(userdata[r][1]) <= email:
					return r + 1
				if int(userdata[l][1]) > email:
					return l
				return r
			if int(userdata[mid][1]) > email:
				r = int(mid)
			else:
				l = int(mid) + 1
			mid = int((r + l) / 2)

	def get_hash(s, capital = 0):
		hashS = 0
		for i in range(0, len(s)):
			tmp = hashS
			if s[i] <= 'Z':
				hashS = (tmp + (ord(s[i]) + capital) * pow[i]) % MOD
			else:
				hashS = (tmp + ord(s[i]) * pow[i]) % MOD
			
		return hashS

	# -------------------- SIGN UP --------------------
	class signup():  
		def __init__(self) -> None:		
		
			self.frame = tk.Frame(root, width=1200, height=675)
			
			tk.Label(self.frame, image=signup_bg).place(x=0,y=0)

			# username
			self.username_entry = tk.Entry(self.frame, font=("Calibri", 13), fg="#646060")
			self.username_entry.focus()
			self.username_entry.place(x=776, y=155, width=366, height=36)

			# email
			self.email_entry = tk.Entry(self.frame, font=("Calibri", 13), fg="#646060")
			self.email_entry.place(x=776, y=255, width=366, height=36)

			# password
			self.password_entry = tk.Entry(self.frame, font=("Calibri", 13), show="•", fg="#646060")
			self.password_entry.place(x=776, y=355, width=366, height=36)
			self.password_state = tk.Button(
				self.frame, 
				image=hide, 
				bd=0, 
				bg="white", 
				activebackground="white", 
				cursor="hand2", 
				command=lambda: show_password(self.password_state, self.password_entry))
			self.password_state.place(x=1100, y=363)
			
			# confirm password
			self.repassword_entry = tk.Entry(self.frame, font=("Calibri", 13), show="•", fg="#646060")
			self.repassword_entry.place(x=776, y=455, width=366, height=36)
			self.repassword_state = tk.Button(
				self.frame, 
				image=hide, 
				bd=0, 
				bg="white", 
				activebackground="white", 
				cursor="hand2", 
				command=lambda: show_password(self.repassword_state, self.repassword_entry))
			self.repassword_state.place(x=1100, y=463)

			# sign up
			self.signup_button = tk.Button(
				self.frame, 
				text="Sign up", 
				font=("Calibri", 25, "bold"), 
				bd=1,
				fg="#ffd300",
				activeforeground="#ffd300",
				bg="#ff1309",
				activebackground="#ff1309",
				cursor="hand2", 
				command=self.process
				)
			self.signup_button.place(x=776, y=535, height=48, width=364)

			# go to log in
			self.go_to_login_button = tk.Button(
				self.frame,
				image=go_back,
				bd=0,
				activebackground="#a1cede",
				cursor="hand2", 
				command=lambda: [delete_errors(self.required_username_error, self.begin_username_error, self.invalid_username_error, self.username_existed_error, self.username_limit_error, 
											self.required_email_error, self.invalid_email_error, self.email_existed_error,
											self.required_password_error, self.invalid_password_error, self.password_limit_error,
											self.required_repassword_error, self.match_repassword_error),
								reset_state(self.password_state, self.repassword_state),
								change_frame(self.frame, log_in.frame, self.username_entry, self.email_entry, self.password_entry, self.repassword_entry)])
			self.go_to_login_button.place(x=741, y=625)	

			# errors messages
			self.required_username_error = tk.Label(self.frame, image=required_username, bd=1, bg="#aadcfe")
			self.begin_username_error = tk.Label(self.frame, image=begin_username, bd=1, bg="#aadcfe")
			self.invalid_username_error = tk.Label(self.frame, image=invalid_username, bd=1, bg="#aadcfe")
			self.username_existed_error = tk.Label(self.frame, image=username_existed, bd=1, bg="#aadcfe")	
			self.username_limit_error = tk.Label(self.frame, image=username_limit, bd=1, bg="#aadcfe")

			self.required_email_error = tk.Label(self.frame, image=required_email, bd=1, bg="#aadcfe")
			self.invalid_email_error = tk.Label(self.frame, image=invalid_email, bd=1, bg="#aadcfe")
			self.email_existed_error = tk.Label(self.frame, image=email_existed, bd=1, bg="#aadcfe")

			self.required_password_error = tk.Label(self.frame, image=required_password, bd=1, bg="#aadcfe")
			self.invalid_password_error = tk.Label(self.frame, image=invalid_password, bd=1, bg="#aadcfe")
			self.password_limit_error = tk.Label(self.frame, image=password_limit, bd=1, bg="#aadcfe")

			self.required_repassword_error = tk.Label(self.frame, image=required_repassword, bd=1, bg="#aadcfe")
			self.match_repassword_error = tk.Label(self.frame, image=match_repassword, bd=1, bg="#aadcfe")

		def process(self):		
			self.username = self.username_entry.get()
			self.required_username_error.place_forget()
			self.begin_username_error.place_forget()
			self.username_limit_error.place_forget()
			self.invalid_username_error.place_forget()
			self.username_existed_error.place_forget()

			self.email = self.email_entry.get()
			self.required_email_error.place_forget()
			self.invalid_email_error.place_forget()
			self.email_existed_error.place_forget()

			self.password = self.password_entry.get()
			self.required_password_error.place_forget()
			self.password_limit_error.place_forget()
			self.invalid_password_error.place_forget()

			self.repassword = self.repassword_entry.get()
			self.required_repassword_error.place_forget()
			self.match_repassword_error.place_forget()

			# username
			if len(self.username) <= 0:
				self.required_username_error.place(x=773, y=193)
				return None
			if len(self.username) > 32:
				self.username_limit_error.place(x=773, y=196)
				return None
			for i in range(0, len(self.username)):
				if invalid_letter(self.username[i]):
					self.invalid_username_error.place(x=773, y=196)
					return None
			if self.username[0] < 'A':
				self.begin_username_error.place(x=773, y=196)
				return None
			if (len(userdata) > 0):
				for i in userdata:
					if i[0] == self.username:
						self.username_existed_error.place(x=773, y=196)
						return None
			
			# email
			check = False
			if len(self.email) <= 0 or len(self.email) > 320:
				self.required_email_error.place(x=773, y=296)
				return None
			for i in range(0, len(self.email)):
				if (invalid_letter(self.email[i]) 
					and not (self.email[i] == '-' or self.email[i] == '_' 
							or ((self.email[i] == '.' or self.email[i] == '@') and i > 0))
					or i > 64):
					self.invalid_email_error.place(x=773, y=296)
					return None
				if  ((self.email[i] == '-' or self.email[i] == '_' or self.email[i] == '.' or self.email[i] == '@')
						and i > 0 and (self.email[i] == self.email[i - 1] or i + 1 == len(self.email))):
					self.invalid_email_error.place(x=773, y=296)
					return None
				if self.email[i] == '@':
					if (len(self.email) - i > 255):
						self.invalid_email_error.place(x=773, y=296)
						return None
					check = True
					exist_letter = False
					i += 1
					if (invalid_letter(self.email[i])):
						self.invalid_email_error.place(x=773, y=296)
						return None
					i += 1
					while i < len(self.email):
						if (invalid_letter(self.email[i]) 
								and not ((self.email[i] == '-' or self.email[i] == '.') 
										and self.email[i] != self.email[i - 1] and i + 1 < len(self.email))):
							self.invalid_email_error.place(x=773, y=296)
							return None
						exist_letter |= self.email[i] >= 'A'
						i += 1
					i -= 1
					while i >= 3 and self.email[i] != '.' and self.email[i] != '@': 
						i -= 1
						exist_letter |= (self.email[i] >= 'A')
					if (i <= 2 or len(self.email) - i - 1 < 2 or self.email[i] != '.' or not exist_letter):
						self.invalid_email_error.place(x=773, y=296)
						return None
					break
			if not check:
				self.invalid_email_error.place(x=773, y=296)
				return None
			self.email_code = get_hash(self.email_entry.get(), 32)
			self.pos = pos_user(self.email_code)
			if (self.pos > 0 and self.email_code == int(userdata[self.pos - 1][1])):
				self.email_existed_error.place(x=773, y=296)
				return None

			# password
			if len(self.password) <= 0:
				self.required_password_error.place(x=773, y=396)
				return None
			if len(self.password) > 16 or len(self.password) < 8:
				self.password_limit_error.place(x=773, y=396)
				return None
			for i in self.password:
				if invalid_letter(i):
					self.invalid_password_error.place(x=773, y=396)
					return None
			
			# confirm password
			if len(self.repassword) <= 0:
				self.required_repassword_error.place(x=773, y=496)
				return None
			if len(self.repassword) != len(self.password) or self.repassword != self.password:
				self.match_repassword_error.place(x=773, y=496)
				return None
			
			# sign up success
			userdata.insert(self.pos - 1, [self.username , self.email_code, get_hash(self.password)])
			trans_str()
			
			delete_errors(self.required_username_error, self.begin_username_error, self.invalid_username_error, self.username_existed_error, self.username_limit_error, 
						self.required_email_error, self.invalid_email_error, self.email_existed_error,
						self.required_password_error, self.invalid_password_error, self.password_limit_error,
						self.required_repassword_error, self.match_repassword_error)
			reset_state(self.password_state, self.repassword_state)
			change_frame(self.frame, log_in.frame, self.username_entry, self.email_entry, self.password_entry, self.repassword_entry)

	# -------------------- LOG IN --------------------
	class login():
		def __init__(self) -> None:
			self.frame = tk.Frame(root, width=1200, height=675)
			
			tk.Label(self.frame, image=login_bg).place(x=0,y=0)

			# username
			self.username_entry = tk.Entry(self.frame, font=("Calibri", 13), fg="#646060")
			self.username_entry.focus()
			self.username_entry.place(x=776, y=155, width=366, height=36)

			# password
			self.password_entry = tk.Entry(self.frame, font=("Calibri", 13), show="•", fg="#646060")
			self.password_entry.place(x=776, y=255, width=366, height=36)
			self.password_state = tk.Button(
				self.frame, 
				image=hide, 
				bd=0, 
				bg="white", 
				activebackground="white", 
				cursor="hand2", 
				command=lambda: show_password(self.password_state, self.password_entry))
			self.password_state.place(x=1100, y=263)

			# log in
			self.login_button = tk.Button(
				self.frame, 
				text="Log in", 
				font=("Calibri", 25, "bold"), 
				bd=1,
				fg="#ffd300",
				activeforeground="#ffd300",
				bg="#ff1309",
				activebackground="#ff1309",
				cursor="hand2", 
				command=self.process
				)
			self.login_button.place(x=776, y=335, height=48, width=364)

			# forgot password
			self.reset_pass = reset_password()
			self.forget_password_button = tk.Button(
				self.frame, 
				image=go_to,
				bd=0,
				activebackground="#a1cede",
				cursor="hand2",
				command=lambda: [delete_errors(self.required_username_error, self.find_username_error,
											self.required_password_error, self.match_password_error),
								reset_state(self.password_state),
								change_frame(self.frame, self.reset_pass.frame, self.username_entry, self.password_entry)])
			self.forget_password_button.place(x=832, y=402)

			# go to sign up
			self.sign_up = signup()
			self.go_to_signup_button = tk.Button(
				self.frame, 
				image=go_to,
				bd=0,
				activebackground="#a1cede",
				cursor="hand2", 
				command=lambda: [delete_errors(self.required_username_error, self.find_username_error,
											self.required_password_error, self.match_password_error),
								reset_state(self.password_state),
								change_frame(self.frame, self.sign_up.frame, self.username_entry, self.password_entry)])
			self.go_to_signup_button.place(x=795, y=434)

			# errors messages
			self.required_username_error = tk.Label(self.frame, image=required_username, bd=1, bg="#aadcfe")
			self.find_username_error = tk.Label(self.frame, image=find_username, bd=1, bg="#aadcfe")
			self.required_password_error = tk.Label(self.frame, image=required_password_login, bd=1, bg="#aadcfe")
			self.match_password_error = tk.Label(self.frame, image=match_password, bd=1, bg="#aadcfe")


		def process(self):
			self.required_username_error.place_forget()
			self.find_username_error.place_forget()
			self.required_password_error.place_forget()
			self.match_password_error.place_forget()

			if len(self.username_entry.get()) <= 0:
				self.required_username_error.place(x=773, y=193)
				return None
			
			self.pos = -1
			for i in range(0, len(userdata)):
				if (userdata[i][0] == self.username_entry.get()):
					self.pos = i
					break
			if self.pos < 0:
				self.find_username_error.place(x=773, y=196)
				return None

			if len(self.password_entry.get()) <= 0:
				self.required_password_error.place(x=774, y=296)
				return None

			if get_hash(self.password_entry.get()) != int(userdata[self.pos][2]):
				self.match_password_error.place(x=773, y=296)
				return None

			# login in successful
			self.play_game()
		
		def play_game(self):
			global pos
			pos = self.pos
			file.close()
			root.destroy()

	class reset_password:
		def __init__(self):		
			self.frame = tk.Frame(root, width=1200, height=675)
			
			tk.Label(self.frame, image=reset_password_bg).place(x=0,y=0)

			# username
			self.username_entry = tk.Entry(self.frame, font=("Calibri", 13), fg="#646060")
			self.username_entry.focus()
			self.username_entry.place(x=776, y=155, width=366, height=36)

			# email
			self.email_entry = tk.Entry(self.frame, font=("Calibri", 13), fg="#646060")
			self.email_entry.place(x=776, y=255, width=366, height=36)

			# password
			self.password_entry = tk.Entry(self.frame, font=("Calibri", 13), show="•", fg="#646060")
			self.password_entry.place(x=776, y=355, width=366, height=36)
			self.password_state = tk.Button(
				self.frame, 
				image=hide, 
				bd=0, 
				bg="white", 
				activebackground="white", 
				cursor="hand2", 
				command=lambda: show_password(self.password_state, self.password_entry))
			self.password_state.place(x=1100, y=363)
			
			# confirm password
			self.repassword_entry = tk.Entry(self.frame, font=("Calibri", 13), show="•", fg="#646060")
			self.repassword_entry.place(x=776, y=455, width=366, height=36)
			self.repassword_state = tk.Button(
				self.frame, 
				image=hide, 
				bd=0, 
				bg="white", 
				activebackground="white", 
				cursor="hand2", 
				command=lambda: show_password(self.repassword_state, self.repassword_entry))
			self.repassword_state.place(x=1100, y=463)

			# reset password
			self.reset_password_button = tk.Button(
				self.frame, 
				text="Reset password", 
				font=("Calibri", 25, "bold"), 
				bd=1,
				fg="#ffd300",
				activeforeground="#ffd300",
				bg="#ff1309",
				activebackground="#ff1309",
				cursor="hand2", 
				command=self.process
				)
			self.reset_password_button.place(x=776, y=535, height=48, width=364)

			# go to log in
			self.go_to_login_button = tk.Button(
				self.frame,
				image=go_back,
				bd=0,
				activebackground="#a1cede",
				cursor="hand2", 
				command=lambda: [delete_errors(self.required_username_error, self.find_username_error,
											self.required_email_error, self.find_email_error,
											self.required_password_error, self.invalid_password_error, self.password_limit_error,
											self.required_repassword_error, self.match_repassword_error),
								reset_state(self.password_state, self.repassword_state),
								change_frame(self.frame, log_in.frame, self.username_entry, self.email_entry, self.password_entry, self.repassword_entry)])
			self.go_to_login_button.place(x=741, y=625)	

			# errors messages
			self.required_username_error = tk.Label(self.frame, image=required_username, bd=1, bg="#aadcfe")
			self.find_username_error = tk.Label(self.frame, image=find_username, bd=1, bg="#aadcfe")
			
			self.required_email_error = tk.Label(self.frame, image=required_email, bd=1, bg="#aadcfe")
			self.find_email_error = tk.Label(self.frame, image=find_email, bd=1, bg="#aadcfe")

			self.required_password_error = tk.Label(self.frame, image=required_password, bd=1, bg="#aadcfe")
			self.invalid_password_error = tk.Label(self.frame, image=invalid_password, bd=1, bg="#aadcfe")
			self.password_limit_error = tk.Label(self.frame, image=password_limit, bd=1, bg="#aadcfe")

			self.required_repassword_error = tk.Label(self.frame, image=required_repassword, bd=1, bg="#aadcfe")
			self.match_repassword_error = tk.Label(self.frame, image=match_repassword, bd=1, bg="#aadcfe")
		
		def process(self):
			self.required_username_error.place_forget()
			self.find_username_error.place_forget()
			self.required_email_error.place_forget()
			self.find_email_error.place_forget()
			self.required_password_error.place_forget()
			self.password_limit_error.place_forget()
			self.invalid_password_error.place_forget()
			self.required_repassword_error.place_forget()
			self.match_repassword_error.place_forget()

			# username
			if len(self.username_entry.get()) <= 0:
				self.required_username_error.place(x=773, y=193)
				return None

			self.pos = -1
			for i in range(0, len(userdata)):
				if userdata[i][0] == self.username_entry.get():
					self.pos = i
					break
			if self.pos < 0:
				self.find_username_error.place(x=773, y=196)
				return None

			# email
			if len(self.email_entry.get()) <= 0:
				self.required_email_error.place(x=773, y=296)
				return None
			self.email_code = get_hash(self.email_entry.get(), 32)
			if (int(userdata[self.pos][1]) != self.email_code):
				self.find_email_error.place(x=773, y=296)
				return None

			# password
			self.password = self.password_entry.get()
			if len(self.password) <= 0:
				self.required_password_error.place(x=773, y=396)
				return None
			if len(self.password) > 16 or len(self.password) < 8:
				self.password_limit_error.place(x=773, y=396)
				return None
			for i in self.password:
				if invalid_letter(i):
					self.invalid_password_error.place(x=773, y=396)
					return None
			
			# confirm password
			self.repassword = self.repassword_entry.get()
			if len(self.repassword) <= 0:
				self.required_repassword_error.place(x=773, y=496)
				return None
			self.password_code = get_hash(self.password)
			if len(self.repassword) != len(self.password) or self.password_code != get_hash(self.repassword):
				self.match_repassword_error.place(x=773, y=496)
				return None
			
			# reset password
			userdata[self.pos - 1][2] = self.password_code
			trans_str()

			delete_errors(self.required_username_error, self.find_username_error,
						self.required_email_error, self.find_email_error,
						self.required_password_error, self.password_limit_error, self.invalid_password_error,
						self.required_repassword_error, self.match_repassword_error)
			reset_state(self.password_state, self.repassword_state)
			change_frame(self.frame, log_in.frame, self.username_entry, self.email_entry, self.password_entry, self.repassword_entry),

	# --------------------------------------------------------------------------------

	prep_hash()
	log_in = login()
	log_in.frame.pack(expand=True, fill="both")

	root.mainloop()

	return pos