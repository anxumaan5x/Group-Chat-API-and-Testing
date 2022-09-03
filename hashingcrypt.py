import bcrypt
  
# example password

def encrypt(password):
    # converting password to array of bytes
    bytes = password.encode('utf-8')  
    # generating the salt
    salt = bcrypt.gensalt()  
    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt)
    value=hash.decode('utf_8')
    return value
# Taking user entered password 

def checkpassword(password, hash):
    userPassword =  password  
    # encoding user password
    userBytes = userPassword.encode('utf-8')
    hash=hash.encode('utf-8')
    
    # checking password
    result = bcrypt.checkpw(userBytes, hash)
    return result


# encrypt("password")
# checkpassword('password', '$2b$12$eWs5xKCNoljiSwGcO65rNuIcg1freaQNaEZw79xqZZjmM3QmOZRaC')