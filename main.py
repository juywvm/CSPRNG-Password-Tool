import os
import sys
import time
import secrets
import string
import subprocess
import ctypes
import glob

if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def copy_text(text):
    try:
        if sys.platform == 'win32':
            subprocess.run('clip', text=True, input=text, shell=True)
        elif sys.platform == 'darwin':
            subprocess.run('pbcopy', text=True, input=text)
        else:
            subprocess.run(['xclip', '-selection', 'clipboard'], text=True, input=text)
        return True
    except Exception:
        return False

def wipe_ram(s):
    if not isinstance(s, str):
        return
    
    length = len(s)
    offset = sys.getsizeof("") - 1
    
    try:
        BUFFER = ctypes.c_char * length
        buffer_ptr = ctypes.cast(id(s) + offset, ctypes.POINTER(BUFFER))
        buffer_ptr.contents.value = secrets.token_bytes(length)
    except Exception:
        pass

def shred_vaults():
    files = glob.glob("secure_key_*.vault")
    for filepath in files:
        try:
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath)
                if file_size > 0:
                    with open(filepath, "wb") as f:
                        f.write(secrets.token_bytes(file_size))
                os.remove(filepath)
        except Exception:
            pass

def ask(prompt, valid_choices):
    while True:
        ans = input(prompt).strip().lower()
        for choice_group in valid_choices:
            if ans in choice_group:
                return choice_group[0]

def generate_pass(length, pool):
    if not pool:
        return ""
    
    password_chars = []
    for _ in range(length):
        random_index = secrets.randbelow(len(pool))
        password_chars.append(pool[random_index])
    
    sys_random = secrets.SystemRandom()
    sys_random.shuffle(password_chars)
    
    return "".join(password_chars)

def save_pass(password):
    filename = f"secure_key_{int(time.time())}.vault"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(password)
    return filename

def main():
    while True:
        choices = []
        pool = ""
        
        clear()
        use_small = ask("do you want to use small characters? (yes/no or y/n)  example: abcdefghijklmnopqrstuvwxyz\n-> ", [['yes', 'y'], ['no', 'n']])
        choices.append(("use small characters", use_small == 'yes'))
        if use_small == 'yes':
            pool += string.ascii_lowercase
            
        clear()
        for name, val in choices:
            print(f"{name}: {str(val).lower()}")
        print()
        use_upper = ask("do you want to use uppercase characters? (yes/no or y/n)  example: ABCDEFGHIJKLMNOPQRSTUVWXYZ\n-> ", [['yes', 'y'], ['no', 'n']])
        choices.append(("use uppercase characters", use_upper == 'yes'))
        if use_upper == 'yes':
            pool += string.ascii_uppercase

        clear()
        for name, val in choices:
            print(f"{name}: {str(val).lower()}")
        print()
        use_symbols = ask("do you want to use symbols? (yes/no or y/n)  example: ~!@#$%^&*+-/.,\\{}[]();:_?<>'\"\n-> ", [['yes', 'y'], ['no', 'n']])
        choices.append(("use symbols", use_symbols == 'yes'))
        if use_symbols == 'yes':
            pool += "~!@#$%^&*+-/.,\\{}[]();:_?<>'\""

        clear()
        for name, val in choices:
            print(f"{name}: {str(val).lower()}")
        print()
        use_numbers = ask("do you want to use numbers? (yes/no or y/n)  example: 1234567890\n-> ", [['yes', 'y'], ['no', 'n']])
        choices.append(("use numbers", use_numbers == 'yes'))
        if use_numbers == 'yes':
            pool += string.digits

        clear()
        for name, val in choices:
            print(f"{name}: {str(val).lower()}")
        print()
        
        alien_prompt = (
            "do you want to use different/alien alphabets?\n"
            "(type 'yes' to mix all, 'no' to skip, 'custom' to select them individually)\n"
            "-> "
        )
        use_alien = ask(alien_prompt, [['yes', 'y'], ['no', 'n'], ['custom', 'c']])
        
        cyrillic = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        devanagari = "अआइईउऊऋएऐओऔकखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह"
        georgian = "აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ"
        amharic = "ሀሁሂሃሄህሆለሉሊላሌልሎሐሑሒሓሔሕሖመሙሚማሜምሞሠሡሢሣሤሥሦረሩሪራሬርሮሰሱሲሳሴስሶ"
        
        choices.append(("use different alphabets", use_alien))
        
        if use_alien == 'yes':
            pool += cyrillic + devanagari + georgian + amharic
            choices.append(("  - included alphabets", "all"))
        elif use_alien == 'custom':
            clear()
            for name, val in choices:
                print(f"{name}: {str(val).lower()}")
            print()
            use_cyrillic = ask("do you want to use russian (cyrillic) characters? (yes/no)\n-> ", [['yes', 'y'], ['no', 'n']])
            choices.append(("  - use russian", use_cyrillic == 'yes'))
            if use_cyrillic == 'yes': pool += cyrillic
            
            clear()
            for name, val in choices:
                print(f"{name}: {str(val).lower()}")
            print()
            use_devanagari = ask("do you want to use hindi (devanagari) characters? (yes/no)\n-> ", [['yes', 'y'], ['no', 'n']])
            choices.append(("  - use hindi", use_devanagari == 'yes'))
            if use_devanagari == 'yes': pool += devanagari
            
            clear()
            for name, val in choices:
                print(f"{name}: {str(val).lower()}")
            print()
            use_georgian = ask("do you want to use georgian (mkhedruli) characters? (yes/no)\n-> ", [['yes', 'y'], ['no', 'n']])
            choices.append(("  - use georgian", use_georgian == 'yes'))
            if use_georgian == 'yes': pool += georgian
            
            clear()
            for name, val in choices:
                print(f"{name}: {str(val).lower()}")
            print()
            use_amharic = ask("do you want to use amharic (ethiopic) characters? (yes/no)\n-> ", [['yes', 'y'], ['no', 'n']])
            choices.append(("  - use amharic", use_amharic == 'yes'))
            if use_amharic == 'yes': pool += amharic

        clear()
        for name, val in choices:
            print(f"{name}: {str(val).lower() if isinstance(val, bool) else val}")
        print()
        
        while True:
            try:
                length_str = input("enter password length (e.g., 64):\n-> ")
                length = int(length_str)
                if length > 0:
                    break
            except ValueError:
                pass
        choices.append(("password length", length))

        clear()
        for name, val in choices:
            print(f"{name}: {str(val).lower() if isinstance(val, bool) else val}")
        print("\ngenerating your password...")
        
        start_time = time.perf_counter()
        
        password = generate_pass(length, pool)
        
        end_time = time.perf_counter()
        time_taken = end_time - start_time
        
        clear()
        for name, val in choices:
            print(f"{name}: {str(val).lower() if isinstance(val, bool) else val}")
        
        print(f"\nyour generated password: {password}")
        print(f"\ntime taken: {time_taken:.10f} seconds")
        
        print("\ntype c or copy to copy your password or manually copy that.")
        print("type s or save to save your password locally.")
        print("type d or delete to securely shred all saved local vault files.")
        print("type r or return to generate another password.")
        
        while True:
            action = input("-> ").strip().lower()
            if action in ['c', 'copy']:
                copy_text(password)
                print("password copied to clipboard!")
            elif action in ['s', 'save']:
                saved_file = save_pass(password)
                print(f"password saved to local directory as {saved_file}")
            elif action in ['d', 'delete']:
                shred_vaults()
                print("all local vault files have been securely shredded and deleted!")
            elif action in ['r', 'return']:
                wipe_ram(password)
                wipe_ram(pool)
                password = None
                pool = None
                break

if __name__ == "__main__":
    main()
