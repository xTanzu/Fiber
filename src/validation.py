from exceptions import CredentialsException, MessageException
import string

username_min_lenght = 6
username_max_lenght = 64
password_min_length = 8
password_max_length = 32
message_max_length = 5;

special_characters = """!()-.?[]_'~;:!@#$%^&*+="""
lowercase_letters = string.ascii_lowercase + "åäö"
uppercase_letters = string.ascii_uppercase + "ÅÄÖ"
letters = lowercase_letters + uppercase_letters

def consists_of_legal_characters(word):
    legal_characters = letters + string.digits + special_characters
    return not any((char not in legal_characters for char in word))

def contains_letters(word):
    return any((char in letters for char in word))

def contains_lowercase_letters(word):
    return any((char in lowercase_letters for char in word))

def contains_uppercase_letters(word):
    return any((char in uppercase_letters for char in word))

def contains_numbers(word):
    return any((char in string.digits for char in word))

def contains_special_characters(word):
    return any((char in special_characters for char in word))

def validate_username(username):
    if not bool(username):
        raise CredentialsException("username is empty")
    if username.isspace():
        raise CredentialsException("username is only space characters")
    if not consists_of_legal_characters(username):
        raise CredentialsException("username contains illegal characters")
    if len(username) < username_min_lenght:
        raise CredentialsException(f"username too short, minimum length of {username_min_lenght} characters")
    if  username_max_lenght < len(username):
        raise CredentialsException(f"username too long, maximum length of {username_max_lenght} characters")
    if contains_special_characters(username[0]):
        raise CredentialsException("username cannot start with a special character")
    if not contains_letters(username):
        raise CredentialsException("username must contain letters")
    return True

def validate_password(password):
    if not bool(password):
        raise CredentialsException("password is empty")
    if password.isspace():
        raise CredentialsException("password is only space characters")
    if not consists_of_legal_characters(password):
        raise CredentialsException("password contains illegal characters")
    if len(password) < password_min_length:
        raise CredentialsException(f"password too short, minimum length of {password_min_length} characters")
    if password_max_length < len(password):
        raise CredentialsException(f"password too long, maximum of {password_max_length} characters")
    if not (contains_lowercase_letters(password) and contains_uppercase_letters(password)):
        raise CredentialsException("password must contain both lower- and uppercase letters")
    if not contains_numbers(password):
        raise CredentialsException("password must contain numbers")
    if not contains_special_characters(password):
        raise CredentialsException("password must contain special characters")
    return True

def validate_message(message):
    if not bool(message):
        raise MessageException("message is empty")
    if message.isspace():
        raise MessageException("message is only space characters")
    if message_max_length < len(message):
        raise MessageException(f"message too long, maximum of {message_max_length} characters")
    return True
