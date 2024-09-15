import math
import customtkinter as ctk
from tkinter import messagebox

# RSA functions
def find_n(modulus, target, exponent):
    for n in range(modulus):
        result = pow(n, exponent, modulus)
        if result == target:
            return n

def RSA_decrypt(enc_message, exponent, modulus):
    try:
        digits = 2 * math.ceil(math.log(modulus, 10) / 2)
        chunks = [enc_message[i:i+digits] for i in range(0, len(enc_message), digits)]
        alpha_index = []
        for chunk in chunks:
            ans = find_n(modulus, int(chunk), exponent)
            formatted_ans = str(ans).zfill(digits)
            alpha_index.append(formatted_ans)
        result = []
        for element in alpha_index:
            result.extend([element[i:i+2] for i in range(0, len(element), 2)])
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        decrypted_message = ''.join(alphabet[int(i)] for i in result)
        return decrypted_message
    except Exception as e:
        return f"Error: {str(e)}"

def binary_array_flipped(num):
    array = []
    while num > 0:
        array.append(num % 2)
        num = num // 2
    return array

def modular_exponentiation(b, e, m):
    x = 1
    p = b % m
    binaries = binary_array_flipped(e)
    for binary in binaries:
        if binary == 1:
            x = (x * p) % m
        p = (p * p) % m
    return x

def split_and_flatten(input_list):
    result = []
    for number in input_list:
        for i in range(0, len(number), 2):
            result.append(number[i:i+2])
    return result

def letter_to_string(letter):
    if 'A' <= letter <= 'Z':
        return f'{ord(letter) - ord("A"):02d}'
    else:
        return '' 

def evaluate_characters(input_strings):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = []
    for string in input_strings:
        positions = [alphabet.index(char) for char in string]
        result.extend(positions)
    return result

def RSA_encrypt(input_str, exponent, n):
    try:
        digits = math.ceil(math.log(n, 10) / 2)
        result = [input_str[i:i+digits] for i in range(0, len(input_str), digits)]
        enc1 = evaluate_characters(result)
        formatted_numbers = [str(num).zfill(2) for num in enc1]
        joined_string = ''.join(formatted_numbers)
        grouped_strings = [joined_string[i:i+(2 * digits)] for i in range(0, len(joined_string), (2 * digits))]
        enc2 = [modular_exponentiation(int(nums), exponent, n) for nums in grouped_strings]
        formatted_ans = [str(num).zfill(2 * digits) for num in enc2]
        return ' '.join(formatted_ans)
    except Exception as e:
        return f"Error: {str(e)}"

# Helper function to show long text in a messagebox
def show_long_message(title, message):
    max_length = 2000  # Set a maximum length for the message box content
    if len(message) > max_length:
        for i in range(0, len(message), max_length):
            messagebox.showinfo(title, message[i:i+max_length])
    else:
        messagebox.showinfo(title, message)

# GUI functions
def encrypt_message():
    try:
        message = entry_encrypt_message.get().upper()
        exponent = int(entry_encrypt_exponent.get())
        modulus = int(entry_encrypt_modulus.get())
        if not message.isalpha():
            raise ValueError("Message must contain only letters.")
        encrypted_message = RSA_encrypt(message, exponent, modulus)
        show_long_message("Encrypted Message", encrypted_message)
    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", str(e))

def decrypt_message():
    try:
        message = entry_decrypt_message.get()
        exponent = int(entry_decrypt_exponent.get())
        modulus = int(entry_decrypt_modulus.get())
        decrypted_message = RSA_decrypt(message, exponent, modulus)
        show_long_message("Decrypted Message", decrypted_message)
    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI setup
app = ctk.CTk()
app.title("RSA Encrypt/Decrypt")

# Encrypt section
frame_encrypt = ctk.CTkFrame(app)
frame_encrypt.pack(padx=10, pady=10, fill='x')

label_encrypt_message = ctk.CTkLabel(frame_encrypt, text="Message:")
label_encrypt_message.grid(row=0, column=0, padx=5, pady=5)
entry_encrypt_message = ctk.CTkEntry(frame_encrypt)
entry_encrypt_message.grid(row=0, column=1, padx=5, pady=5)

label_encrypt_exponent = ctk.CTkLabel(frame_encrypt, text="Exponent:")
label_encrypt_exponent.grid(row=1, column=0, padx=5, pady=5)
entry_encrypt_exponent = ctk.CTkEntry(frame_encrypt)
entry_encrypt_exponent.grid(row=1, column=1, padx=5, pady=5)

label_encrypt_modulus = ctk.CTkLabel(frame_encrypt, text="Modulus:")
label_encrypt_modulus.grid(row=2, column=0, padx=5, pady=5)
entry_encrypt_modulus = ctk.CTkEntry(frame_encrypt)
entry_encrypt_modulus.grid(row=2, column=1, padx=5, pady=5)

button_encrypt = ctk.CTkButton(frame_encrypt, text="Encrypt", command=encrypt_message)
button_encrypt.grid(row=3, column=0, columnspan=2, pady=10)

# Decrypt section
frame_decrypt = ctk.CTkFrame(app)
frame_decrypt.pack(padx=10, pady=10, fill='x')

label_decrypt_message = ctk.CTkLabel(frame_decrypt, text="Encrypted Message:")
label_decrypt_message.grid(row=0, column=0, padx=5, pady=5)
entry_decrypt_message = ctk.CTkEntry(frame_decrypt)
entry_decrypt_message.grid(row=0, column=1, padx=5, pady=5)

label_decrypt_exponent = ctk.CTkLabel(frame_decrypt, text="Exponent:")
label_decrypt_exponent.grid(row=1, column=0, padx=5, pady=5)
entry_decrypt_exponent = ctk.CTkEntry(frame_decrypt)
entry_decrypt_exponent.grid(row=1, column=1, padx=5, pady=5)

label_decrypt_modulus = ctk.CTkLabel(frame_decrypt, text="Modulus:")
label_decrypt_modulus.grid(row=2, column=0, padx=5, pady=5)
entry_decrypt_modulus = ctk.CTkEntry(frame_decrypt)
entry_decrypt_modulus.grid(row=2, column=1, padx=5, pady=5)

button_decrypt = ctk.CTkButton(frame_decrypt, text="Decrypt", command=decrypt_message)
button_decrypt.grid(row=3, column=0, columnspan=2, pady=10)

app.mainloop()

    
# RSA_decrypt("197484035654125328101328186744015511068158101168230573", 241, 521 * 523)
# RSA_encrypt("ATTACK", 13, 43 * 59)