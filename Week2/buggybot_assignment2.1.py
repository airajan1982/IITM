print("Welcome to BuggyBot! (type 'bye' to exit)")

user_input = ""   # Initialize
while user_input != "bye":
    user_input = input("You: ").lower()  # Convert input to lowercase for easier comparison  

    #if user_input == "hi" or "hello": Bot corrected this line.
    if user_input == "hi" or user_input == "hello":
        print("Bot: Hello there!")
    elif user_input == "bye":
        print("Bot: Goodbye!")
    else:
        print("Bot: I don’t understand.")


#     Trace the value of user_input at each iteration of the loop when the following inputs are entered in order: hi, hello, bye. Fill in the table below:

# Iteration	User Input	Value of user_input	ChatGPT Response
# 1	        hi	        "hi"                Bot: Hello there!	
# 2	        hello		"hello"             Bot: Hello there!
# 3	        bye		    "bye"               Bot: Goodbye!
 