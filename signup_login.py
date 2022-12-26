import tkinter as tk

userdata = []
pow = []
MOD = int(1e9) + 9277

def prep_hash():
	BASE = 256
	MAX = 320

	global pow, MOD

	pow.append(1)
	for i in range(1, MAX):
		pow.append(pow[i - 1] * BASE % MOD)

def trans_list(data):
	global userdata
	for line in data:
		number = 0
		tmp = []
		for i in range(0, len(line) - 1):
			if line[i] == '[': 
				continue
			if line[i] == ' ' or line[i] == ']':
				tmp.append(number)
				number = 0
			else: 
				number = number * 10 + int(line[i])
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
# root.resizable(False, False)
root.iconbitmap("./asset/image/logo.ico")
root.title("Life is a lie")

show = tk.PhotoImage(file="./asset/image/show.png")
hide = tk.PhotoImage(file="./asset/image/hide.png")

# --------------------------------------------------------------------------------

def change_frame(src, des):
	src.forget()
	des.pack(side="right")

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

def pos_username(username):
	global userdata

	l = int(0)
	r = len(userdata) - 1
	mid = int((r + l) / 2)
	
	if (r < 0): 
		return -1

	while (True):
		if l + 1 >= r:
			if userdata[r][0] <= username:
				return r + 1
			if userdata[l][0] > username:
				return l
			return r
		if userdata[mid][0] > username:
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
		global log_in
		
		self.frame = tk.Frame(root, width=600, height=675)
		
		tk.Label(self.frame, text="Join Life is a lie", font=("Calibria", 30, "bold")).grid(column=0, row=0, padx=60, pady=10, sticky="N")

		# username
		tk.Label(self.frame, text="Username", font=("Calibri", 15, "bold")).grid(column=0, row=1, pady=5, ipadx=50, sticky="W")
		self.username_entry = tk.Entry(self.frame, font=("Calibri", 13), width=25)
		self.username_entry.grid(column=0, row=2, padx=50, pady=5, ipadx=92, ipady=6, sticky="W")
		self.username_entry.focus()

		# email
		tk.Label(self.frame, text="Email", font=("Calibri", 15, "bold")).grid(column=0, row=4, pady=5, ipadx=50, sticky="W")
		self.email_entry = tk.Entry(self.frame, font=("Calibri", 13), width=25)
		self.email_entry.grid(column=0, row=5, padx=50, pady=5, ipadx=92, ipady=6, sticky="W")

		# password
		tk.Label(self.frame, text="Password", font=("Calibri", 15, "bold")).grid(column=0, row=7, pady=7, ipadx=50, sticky="W")
		self.password_entry = tk.Entry(self.frame, font=("Calibri", 13), width=25, show="•")
		self.password_entry.grid(column=0, row=8, padx=50, pady=5, ipadx=92, ipady=6, sticky="W")
		self.password_state = tk.Button(
			self.frame, 
			image=hide, 
			bd=0, 
			bg="white", 
			activebackground="white", 
			cursor="hand2", 
			command=lambda: show_password(self.password_state, self.password_entry))
		self.password_state.grid(column=0, row=8, padx=60, sticky="E")
		
		# confirm password
		tk.Label(self.frame, text="Confirm password", font=("Calibri", 15, "bold")).grid(column=0, row=10, pady=5, ipadx=50, sticky="W")
		self.repassword_entry = tk.Entry(self.frame, font=("Calibri", 13), width=25, show="•")
		self.repassword_entry.grid(column=0, row=11, padx=50, pady=5, ipadx=92, ipady=6, sticky="W")
		self.repassword_state = tk.Button(
			self.frame, 
			image=hide, 
			bd=0, 
			bg="white", 
			activebackground="white", 
			cursor="hand2", 
			command=lambda: show_password(self.repassword_state, self.repassword_entry))
		self.repassword_state.grid(column=0, row=11, padx=60, sticky="E")

		# sign up
		self.signup_button = tk.Button(
			self.frame, 
			text="Sign up", 
			font=("Calibri", 25, "bold"), 
			cursor="hand2", 
			bd=1, 
			bg="black", 
			foreground="white", 
			activebackground="black", 
			width=24, 
			command=self.process)
		self.signup_button.grid(column=0, row=13, pady=15)

		# go to log in
		self.go_to_login_button = tk.Button(
			self.frame, 
			text="Already have an account? Log in.", 
			font=("Calibri", 13, "italic underline"), 
			bd=0, 
			cursor="hand2", 
			command=lambda: change_frame(self.frame, log_in.frame))
		self.go_to_login_button.grid(column=0, row=15, pady=5)	

		# errors messages
		self.required_username_error = tk.Label(self.frame, text="Username is required.", font=("Calibri", 11), fg="red")
		self.begin_username_error = tk.Label(self.frame, text="Sorry, username must begin with a letter (a-z, A-Z).", font=("Calibri", 11), fg="red")
		self.invalid_username_error = tk.Label(self.frame, text="Sorry, only letters (A-Z, a-z), and numbers (0-9) are allowed.", font=("Calibri", 11), fg="red")
		self.username_existed_error = tk.Label(self.frame, text="Username is already in use. Please try another name.", font=("Calibri", 12), fg="red")	
		self.limit_username_error = tk.Label(self.frame, text="Username value length exceeds 32 characters.", font=("Calibri", 12), fg="red")	

		self.required_email_error = tk.Label(self.frame, text="Email is required.", font=("Calibri", 11), fg="red")
		self.invalid_email_error = tk.Label(self.frame, text="The email address is invalid.", font=("Calibri", 11), fg="red")
		self.email_existed_error = tk.Label(self.frame, text="That email address is already in registered.", font=("Calibri", 12), fg="red")	

		self.required_password_error = tk.Label(self.frame, text="Password is required.", font=("Calibri", 11), fg="red")
		self.invalid_password_error = tk.Label(self.frame, text="Sorry, only letters (A-Z, a-z) and numbers (0-9) are allowed.", font=("Calibri", 11), fg="red")
		self.limit_password_error = tk.Label(self.frame, text="Password value length exceeds 16 characters.", font=("Calibri", 12), fg="red")	

		self.required_repassword_error = tk.Label(self.frame, text="Confirm password is required.", font=("Calibri", 11), fg="red")
		self.match_repassword_error = tk.Label(self.frame, text="Passwords do not match.", font=("Calibri", 11), fg="red")

	def process(self):		
		global userdata, log_in
		
		self.username = self.username_entry.get()
		self.required_username_error.grid_forget()
		self.begin_username_error.grid_forget()
		self.limit_username_error.grid_forget()
		self.invalid_username_error.grid_forget()
		self.username_existed_error.grid_forget()

		self.email = self.email_entry.get()
		self.required_email_error.grid_forget()
		self.invalid_email_error.grid_forget()
		self.email_existed_error.grid_forget()

		self.password = self.password_entry.get()
		self.required_password_error.grid_forget()
		self.limit_password_error.grid_forget()
		self.invalid_password_error.grid_forget()

		self.repassword = self.repassword_entry.get()
		self.required_repassword_error.grid_forget()
		self.match_repassword_error.grid_forget()

		# username
		if len(self.username) <= 0:
			self.required_username_error.grid(column=0, row=3, pady=5, ipadx=50, sticky="W")
			return None
		if len(self.username) > 32:
			self.limit_username_error.grid(column=0, row=3, pady=5, ipadx=50, sticky="W")
			return None
		if self.username[0] < 'A':
			self.begin_username_error.grid(column=0, row=3, pady=5, ipadx=50, sticky="W")
			return None
		for i in range(0, len(self.username)):
			if invalid_letter(self.username[i]):
				self.invalid_username_error.grid(column=0, row=3, pady=5, ipadx=50, sticky="W")
				return None
		self.username_code = get_hash(self.username)
		pos = pos_username(self.username_code)
		if (pos > 0 and self.username_code == userdata[pos - 1][0]):
			self.username_existed_error.grid(column=0, row=3, pady=5, ipadx=50, sticky="W")
			return None
		
		# email
		check = False
		if len(self.email) <= 0 or len(self.email) > 320:
			self.required_email_error.grid(column=0, row=6, pady=5, ipadx=50, sticky="W")
			return None
		for i in range(0, len(self.email)):
			if (invalid_letter(self.email[i]) 
				and not (self.email[i] == '-' or self.email[i] == '_' 
						or ((self.email[i] == '.' or self.email[i] == '@') and i > 0))
				or i >= 64):
				self.invalid_email_error.grid(column=0, row=6, pady=5, ipadx=50, sticky="W")
				return None
			if  ((self.email[i] == '-' or self.email[i] == '_' or self.email[i] == '.' or self.email[i] == '@')
					and i > 0 and (self.email[i] == self.email[i - 1] or i + 1 == len(self.email))):
				self.invalid_email_error.grid(column=0, row=6, pady=5, ipadx=50, sticky="W")
				return None
			if self.email[i] == '@':
				if (len(self.email) - i > 255):
					self.invalid_email_error.grid(column=0, row=6, pady=5, ipadx=50, sticky="W")
					return None
				check = True
				exist_letter = False
				i += 1
				if (invalid_letter(self.email[i])):
					self.invalid_email_error.grid(column=0, row=6, pady=5, ipadx=50, sticky="W")
					return None
				i += 1
				while i < len(self.email):
					if (invalid_letter(self.email[i]) 
							and not ((self.email[i] == '-' or self.email[i] == '.') 
									and self.email[i] != self.email[i - 1] and i + 1 < len(self.email))):
						self.invalid_email_error.grid(column=0, row=6, pady=5, ipadx=50, sticky="W")
						return None
					exist_letter |= self.email[i] >= 'A'
					i += 1
				i -= 1
				while i >= 3 and self.email[i] != '.' and self.email[i] != '@': 
					i -= 1
					exist_letter |= (self.email[i] >= 'A')
				if (i <= 2 or len(self.email) - i - 1 < 2 or self.email[i] != '.' or not exist_letter):
					self.invalid_email_error.grid(column=0, row=6, pady=5, ipadx=50, sticky="W")
					return None
				break
		if not check:
			self.invalid_email_error.grid(column=0, row=6, pady=5, ipadx=50, sticky="W")
			return None
		self.email_code = get_hash(self.email, 32)
		if len(userdata) > 0:
			for i in userdata:
				if self.email_code == i[1]:
					self.email_existed_error.grid(column=0, row=6, pady=5, ipadx=50, sticky="W")
					return None

		# password
		if len(self.password) <= 0:
			self.required_password_error.grid(column=0, row=9, pady=5, ipadx=50, sticky="W")
			return None
		if len(self.password) > 16:
			self.limit_password_error.grid(column=0, row=9, pady=5, ipadx=50, sticky="W")
			return None
		for i in self.password:
			if invalid_letter(i):
				self.invalid_password_error.grid(column=0, row=9, pady=5, ipadx=50, sticky="W")
				return None
		
		# confirm password
		if len(self.repassword) <= 0:
			self.required_repassword_error.grid(column=0, row=12, pady=5, ipadx=50, sticky="W")
			return None
		self.password_code = get_hash(self.password)
		if len(self.repassword) != len(self.password) or self.password_code != get_hash(self.repassword):
			self.match_repassword_error.grid(column=0, row=12, pady=5, ipadx=50, sticky="W")
			return None
		
		# sign up success
		userdata.insert(pos, [self.username_code , self.email_code, self.password_code])
		trans_str()
		
		change_frame(self.frame, log_in.frame)

# -------------------- LOG IN --------------------
class login():
	def __init__(self) -> None:
		self.frame = tk.Frame(root, width=600, height=675)
		self.frame.pack(side="right")
		
		tk.Label(self.frame, text="Log in to Life is a lie", font=("Calibria", 30, "bold")).grid(column=0, row=0, padx=30, pady=20, sticky="N")

		# username
		tk.Label(self.frame, text="Username", font=("Calibri", 15, "bold")).grid(column=0, row=1, padx=80, pady=5, sticky="W")
		self.username_entry = tk.Entry(self.frame, font=("Calibri", 13), width=25)
		self.username_entry.focus()
		self.username_entry.grid(column=0, row=2, padx=80, pady=5, ipadx=92, ipady=6, sticky="W")

		# password
		tk.Label(self.frame, text="Password", font=("Calibri", 15, "bold")).grid(column=0, row=4, padx=80, pady=5, sticky="W")
		self.password_entry = tk.Entry(self.frame, font=("Calibri", 13), width=25, show="•")
		self.password_entry.grid(column=0, row=5, padx=80, pady=5, ipadx=92, ipady=6, sticky="W")
		self.password_state = tk.Button(
			self.frame, 
			image=hide, 
			bd=0, 
			bg="white", 
			activebackground="white", 
			cursor="hand2", 
			command=lambda: show_password(self.password_state, self.password_entry))
		self.password_state.grid(column=0, row=5, padx=90, sticky="E")

		# log in
		self.login_button = tk.Button(
			self.frame, 
			text="Log in", 
			font=("Calibri", 25, "bold"), 
			cursor="hand2", bd=1, 
			bg="black", 
			foreground="white", 
			activebackground="black", 
			width=24, 
			command=self.process)
		self.login_button.grid(column=0, row=7, pady=15)

		# forget password
		self.reset_pass = reset_password()
		self.forget_password_button = tk.Button(
			self.frame, 
			text="Forgot password?", 
			font=("Calibri", 13, "bold"), 
			bd=0, 
			cursor="hand2",
			command=lambda: change_frame(self.frame, self.reset_pass.frame))
		self.forget_password_button.grid(column=0, row=8)

		# go to sign up
		self.sign_up = signup()
		self.go_to_signup_button = tk.Button(
			self.frame, 
			text="Don't have an account? Sign up.", 
			font=("Calibri", 13, "italic underline"), 
			bd=0, 
			cursor="hand2", 
			command=lambda: change_frame(self.frame, self.sign_up.frame))
		self.go_to_signup_button.grid(column=0, row=9)

		# errors messages
		self.required_username_error = tk.Label(self.frame, text="Username is required.", font=("Calibri", 11), fg="red")
		self.required_password_error = tk.Label(self.frame, text="Password is required.", font=("Calibri", 11), fg="red")
		self.find_username_error = tk.Label(self.frame, text="Username doesn't exist.", font=("Calibri", 11), fg="red")
		self.match_password_error = tk.Label(self.frame, text="The username or password is incorrect.", font=("Calibri", 11), fg="red")
	
	def process(self):
		global userdata

		self.required_username_error.grid_forget()
		self.required_password_error.grid_forget()
		self.find_username_error.grid_forget()
		self.match_password_error.grid_forget()

		if len(self.username_entry.get()) <= 0:
			self.required_username_error.grid(column=0, row=3, padx=80, pady=5, sticky="W")
			return None
		
		self.username_code = get_hash(self.username_entry.get())
		self.pos = pos_username(self.username_code)
		if self.pos <= 0 or self.pos > len(userdata) or userdata[self.pos - 1][0] != self.username_code:
			self.find_username_error.grid(column=0, row=3, padx=80, pady=5, sticky="W")
			return None

		if len(self.password_entry.get()) <= 0:
			self.required_password_error.grid(column=0, row=6, padx=80, pady=5, sticky="W")
			return None

		self.password_code = get_hash(self.password_entry.get())
		if self.password_code != userdata[self.pos - 1][2]:
			self.match_password_error.grid(column=0, row=6, padx=80, pady=5, sticky="W")
			return None

		# login in successful
		self.play_game()

	def play_game(self):
		file.close()
		root.destroy()
		import main2 

class reset_password:
	def __init__(self):
		global log_in
		
		self.frame = tk.Frame(root, width=600, height=675)
		
		tk.Label(self.frame, text="Lost your password?", font=("Calibria", 30, "bold")).grid(column=0, row=0, padx=60, pady=10, sticky="N")

		# username
		tk.Label(self.frame, text="Username", font=("Calibri", 15, "bold")).grid(column=0, row=1, pady=5, ipadx=50, sticky="W")
		self.username_entry = tk.Entry(self.frame, font=("Calibri", 13), width=25)
		self.username_entry.grid(column=0, row=2, padx=50, pady=5, ipadx=92, ipady=6, sticky="W")
		self.username_entry.focus()

		# email
		tk.Label(self.frame, text="Email", font=("Calibri", 15, "bold")).grid(column=0, row=4, pady=5, ipadx=50, sticky="W")
		self.email_entry = tk.Entry(self.frame, font=("Calibri", 13), width=25)
		self.email_entry.grid(column=0, row=5, padx=50, pady=5, ipadx=92, ipady=6, sticky="W")

		# password
		tk.Label(self.frame, text="New password", font=("Calibri", 15, "bold")).grid(column=0, row=7, pady=7, ipadx=50, sticky="W")
		self.password_entry = tk.Entry(self.frame, font=("Calibri", 13), width=25, show="•")
		self.password_entry.grid(column=0, row=8, padx=50, pady=5, ipadx=92, ipady=6, sticky="W")
		self.password_state = tk.Button(
			self.frame, 
			image=hide, 
			bd=0, 
			bg="white", 
			activebackground="white", 
			cursor="hand2", 
			command=lambda: show_password(self.password_state, self.password_entry))
		self.password_state.grid(column=0, row=8, padx=70, sticky="E")
		
		# confirm password
		tk.Label(self.frame, text="Confirm new password", font=("Calibri", 15, "bold")).grid(column=0, row=10, pady=5, ipadx=50, sticky="W")
		self.repassword_entry = tk.Entry(self.frame, font=("Calibri", 13), width=25, show="•")
		self.repassword_entry.grid(column=0, row=11, padx=50, pady=5, ipadx=92, ipady=6, sticky="W")
		self.repassword_state = tk.Button(
			self.frame, 
			image=hide, 
			bd=0, 
			bg="white", 
			activebackground="white", 
			cursor="hand2", 
			command=lambda: show_password(self.repassword_state, self.repassword_entry))
		self.repassword_state.grid(column=0, row=11, padx=70, sticky="E")

		# reset password
		self.signup_button = tk.Button(
			self.frame, 
			text="Reset password", 
			font=("Calibri", 25, "bold"), 
			cursor="hand2", 
			bd=1, 
			bg="black", 
			foreground="white", 
			activebackground="black", 
			width=24, 
			command=self.process)
		self.signup_button.grid(column=0, row=13, pady=15)

		# back to log in
		self.go_to_login_button = tk.Button(
			self.frame, 
			text="< Back", 
			font=("Calibri", 13, "bold underline"), 
			cursor="hand2", 
			bd=0, 
			command=lambda: change_frame(self.frame, log_in.frame))
		self.go_to_login_button.grid(column=0, row=14, padx=60, pady=5, sticky="W")	
	
		# errors messages
		self.required_username_error = tk.Label(self.frame, text="Username is required.", font=("Calibri", 11), fg="red")
		self.find_username_error = tk.Label(self.frame, text="Username doesn't exist.", font=("Calibri", 11), fg="red")

		self.required_email_error = tk.Label(self.frame, text="Email is required.", font=("Calibri", 11), fg="red")
		self.find_email_error = tk.Label(self.frame, text="The username or email is incorrect.", font=("Calibri", 12), fg="red")	

		self.required_password_error = tk.Label(self.frame, text="Password is required.", font=("Calibri", 11), fg="red")
		self.limit_password_error = tk.Label(self.frame, text="Password value length exceeds 16 characters.", font=("Calibri", 12), fg="red")	
		self.invalid_password_error = tk.Label(self.frame, text="Sorry, only letters (A-Z, a-z) and numbers (0-9) are allowed.", font=("Calibri", 11), fg="red")

		self.required_repassword_error = tk.Label(self.frame, text="Confirm password is required.", font=("Calibri", 11), fg="red")
		self.match_repassword_error = tk.Label(self.frame, text="Passwords do not match.", font=("Calibri", 11), fg="red")
	
	def process(self):
		global userdata, log_in, info

		self.required_username_error.grid_forget()
		self.find_username_error.grid_forget()
		self.required_email_error.grid_forget()
		self.find_email_error.grid_forget()
		self.required_password_error.grid_forget()
		self.limit_password_error.grid_forget()
		self.invalid_password_error.grid_forget()
		self.required_repassword_error.grid_forget()
		self.match_repassword_error.grid_forget()

		# username
		if len(self.username_entry.get()) <= 0:
			self.required_username_error.grid(column=0, row=3, padx=50, pady=5, sticky="W")
			return None
		self.username_code = get_hash(self.username_entry.get())
		self.pos = pos_username(self.username_code)
		if (self.pos <= 0 or self.pos > len(userdata) or userdata[self.pos - 1][0] != self.username_code):
			self.find_username_error.grid(column=0, row=3, padx=50, pady=5, sticky="W")
			return None

		# email
		if len(self.email_entry.get()) <= 0:
			self.required_email_error.grid(column=0, row=6, padx=50, pady=5, sticky="W")
			return None
		self.email_code = get_hash(self.email_entry.get(), 32)
		if (userdata[self.pos - 1][1] != self.email_code):
			self.find_email_error.grid(column=0, row=6, padx=50, pady=5, sticky="W")
			return None

		# password
		self.password = self.password_entry.get()
		if len(self.password) <= 0:
			self.required_password_error.grid(column=0, row=9, padx=50, pady=5, sticky="W")
			return None
		if len(self.password) > 16:
			self.limit_password_error.grid(column=0, row=9, padx=50, pady=5, sticky="W")
			return None
		for i in self.password:
			if invalid_letter(i):
				self.invalid_password_error.grid(column=0, row=9, padx=50, pady=5, sticky="W")
				return None
		
		# confirm password
		self.repassword = self.repassword_entry.get()
		if len(self.repassword) <= 0:
			self.required_repassword_error.grid(column=0, row=12, padx=50, pady=5, sticky="W")
			return None
		self.password_code = get_hash(self.password)
		if len(self.repassword) != len(self.password) or self.password_code != get_hash(self.repassword):
			self.match_repassword_error.grid(column=0, row=12, padx=50, pady=5, sticky="W")
			return None
		
		# reset password
		userdata[self.pos - 1][2] = self.password_code
		trans_str()

		change_frame(self.frame, log_in.frame)

# --------------------------------------------------------------------------------

prep_hash()
log_in = login()

root.mainloop()