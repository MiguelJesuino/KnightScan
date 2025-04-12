import argparse
from Scanner import threaded_scan
import os
import time
import json
from colorama import init, Fore, Style
init(autoreset=True)

def parse_ports(port_str):
    if '-' in port_str:
        # o argumento que estou recebendo no terminal é assim: primeiraPorta-UltimaPorta
        # pra transformar isso em algo legivel pro python tenho que tirar esse "-" e transformar o range de portas em uma lista de portas
        # para isso uso o strip pra tirar o traço, coloco o valor inicial em uma variavel e o valor final em outra
        # depois retorno uma lista de elementos usando list(range(valorInicial, valorFinal+1)) o +1 é pq o range termina 1 numero antes do valor final
        start, end = map(int, port_str.split('-'))
        return list(range(start, end+1))
    else:
        # caso não tenha o traço significa que não é um range de portas e sim uma porta única, sendo assim não precisa de tratamento
        return [int(port_str)]


# Função para salvar os resultados em arquivo
def save_results(results, filename):
    if filename.lower().endswith('.json'):
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)
    else:
        with open(filename, 'w') as f:
            for host, items in results.items():
                f.write(f"\nResultado para {host}:\n")
                if items:
                    for item in items:
                        line = f"Porta {item['port']}: Banner: {item['banner']} | OS: {item['os']}\n"
                        f.write(line)
                else:
                    f.write("Nenhuma porta aberta encontrada.\n")
    print(f"✅ Resultados salvos em {filename}")


if __name__ == "__main__":
    os.system("@echo off")
    os.system("cls")
    print(Fore.RED + r"""
  _____________________________________________________|_,_,_,_,_,_,_,_,_,_,    
/______________________________________________________||#|#|#|#|#|#|#|#|#|#
'------------------------------------------------------|-'-'-'-'-'-'-'-'-'-'
     ____  __.      .__       .__     __   _________                     
    |    |/ _| ____ |__| ____ |  |___/  |_/   _____/ ____ _____    ____  
    |      <  /    \|  |/ ___\|  |  \   __\_____  \_/ ___\\__  \  /    \ 
    |    |  \|   |  \  / /_/  >   Y  \  | /        \  \___ / __ \|   |  \
    |____|__ \___|  /__\___  /|___|  /__|/_______  /\___  >____  /___|  /
            \/    \/  /_____/      \/            \/     \/     \/     \/ 
               
,_,_,_,_,_,_,_,_,_,_|______________________________________________________
|#|#|#|#|#|#|#|#|#|#|_____________________________________________________/
'-'-'-'-'-'-'-'-'-'-|----------------------------------------------------'
                
    """)
    # pegando os argumentos via terminal
    parser = argparse.ArgumentParser(description="Port Scanner Avançado")
    parser.add_argument("hosts", type=str, help="Host(s) alvo (IP ou domínio). Se múltiplos, separe por vírgula")
    parser.add_argument("-p", "--ports", type=str, default="1-1024", help="Porta única ou intervalo (ex: 80 ou 1-1000)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Número de threads (padrão: 100)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Timeout para conexão (padrão: 1 segundo)")
    parser.add_argument("--log", action="store_true", help="Mostrar log completo (incluindo portas fechadas)")
    parser.add_argument("--save", type=str, help="Salvar resultados no arquivo (ex: resultados.txt ou resultados.json)")
    args = parser.parse_args()

    # Processa os hosts (separados por vírgula) e as portas
    hosts = [host.strip() for host in args.hosts.split(",")]
    ports = parse_ports(args.ports)

    print("=" * 80)
    print(f"Escaneando hosts: {', '.join(hosts)}")
    print(f"Portas: {ports[0]} até {ports[-1]} | Threads: {args.threads} | Timeout {args.timeout}s")
    print("=" * 80)

    all_results = {}

    start_time = time.time()

    try:
        for host in hosts:
            print(f"\nIniciando scan em {host}...")
            results = threaded_scan(host, ports, num_threads=args.threads, timeout=args.timeout, show_logs=args.log)
            all_results[host] = results
            print(f"Fim do scan em {host}. {len(results)} portas abertas encontradas.")
    except KeyboardInterrupt:
        print(f"\nScan interrompido pelo usuário. Encerrando...")
        exit(0)

    end_time = time.time()
    total_time = end_time - start_time

    print("=" * 80)
    print(f"Tempo total de scan: {total_time:.2f} segundos")
    print("=" * 80)

    # Salvar resultados se solicitado
    if args.save:
        save_results(all_results, args.save)
