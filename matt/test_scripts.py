# Testing how variable values are stored when overwritten in a function and then recalled in the outer scope
def foo(word_to_say):
    print(word_to_say)
    word_to_say = "No"
    print(word_to_say)

word_to_say = "hello"
foo(word_to_say)
print(word_to_say)
