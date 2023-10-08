import string

name_min_lenght = 6
name_max_lenght = 64
password_min_length = 8
password_max_length = 32
text_max_length = 5000;

special_characters = """!()-.?[]_'~;:!@#$%^&*+="""
lowercase_letters = string.ascii_lowercase + "åäö"
uppercase_letters = string.ascii_uppercase + "ÅÄÖ"
letters = lowercase_letters + uppercase_letters

def consists_of_legal_characters(word, exra_chars=""):
    legal_characters = letters + string.digits + special_characters + exra_chars
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

def validate_name(name, name_type="", exra_chars=""):
    if not bool(name):
        raise ValueError(f"{name_type}name is empty")
    if name.isspace():
        raise ValueError(f"{name_type}name is only space characters")
    if not consists_of_legal_characters(name, exra_chars):
        raise ValueError(f"{name_type}name contains illegal characters")
    if len(name) < name_min_lenght:
        raise ValueError(f"{name_type}name too short, minimum length of {name_min_lenght} characters")
    if  name_max_lenght < len(name):
        raise ValueError(f"{name_type}name too long, maximum length of {name_max_lenght} characters")
    if contains_special_characters(name[0]):
        raise ValueError(f"{name_type}name cannot start with a special character")
    if not contains_letters(name):
        raise ValueError(f"{name_type}name must contain letters")
    return True

def validate_password(password):
    if not bool(password):
        raise ValueError("password is empty")
    if password.isspace():
        raise ValueError("password is only space characters")
    if not consists_of_legal_characters(password):
        raise ValueError("password contains illegal characters")
    if len(password) < password_min_length:
        raise ValueError(f"password too short, minimum length of {password_min_length} characters")
    if password_max_length < len(password):
        raise ValueError(f"password too long, maximum of {password_max_length} characters")
    if not (contains_lowercase_letters(password) and contains_uppercase_letters(password)):
        raise ValueError("password must contain both lower- and uppercase letters")
    if not contains_numbers(password):
        raise ValueError("password must contain numbers")
    if not contains_special_characters(password):
        raise ValueError("password must contain special characters")
    return True

def validate_text(text, text_type=""):
    if not bool(text):
        raise ValueError(f"{text_type if text_type else 'text'} is empty")
    if text.isspace():
        raise ValueError(f"{text_type if text_type else 'text'} is only space characters")
    if text_max_length < len(text):
        raise ValueError(f"{text_type if text_type else 'text'} too long, maximum of {text_max_length} characters")
    return True
