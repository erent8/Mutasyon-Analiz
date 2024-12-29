import csv
import pandas as pd
import matplotlib.pyplot as plt
from difflib import SequenceMatcher

def get_dna_sequences():
    """
    Kullanıcıdan iki DNA dizisi alır.

    Returns:
        tuple: İki DNA dizisini içeren tuple (dna1, dna2).
    """
    dna1 = input("Birinci DNA dizisini girin: ").upper()
    dna2 = input("İkinci DNA dizisini girin: ").upper()
    return dna1, dna2

def check_length(dna1, dna2):
    """
    İki DNA dizisinin uzunluklarının eşit olup olmadığını kontrol eder.

    Args:
        dna1 (str): Birinci DNA dizisi.
        dna2 (str): İkinci DNA dizisi.

    Returns:
        bool: Uzunluklar eşitse True, değilse False.
    """
    return len(dna1) == len(dna2)

def align_and_identify_mutations(dna1, dna2):
    """
    İki farklı uzunluktaki DNA dizisini hizalayarak mutasyon türlerini bulur.

    Args:
        dna1 (str): Birinci DNA dizisi.
        dna2 (str): İkinci DNA dizisi.

    Returns:
        list: Her mutasyon için pozisyon, orijinal, mutasyonlu ve tür bilgisi.
    """
    matcher = SequenceMatcher(None, dna1, dna2)
    mutations = []

    for opcode in matcher.get_opcodes():
        tag, a0, a1, b0, b1 = opcode
        if tag == 'replace':
            mutations.append((a0 + 1, dna1[a0:a1], dna2[b0:b1], 'Replace'))
        elif tag == 'delete':
            mutations.append((a0 + 1, dna1[a0:a1], '-', 'Deletion'))
        elif tag == 'insert':
            mutations.append((a0 + 1, '-', dna2[b0:b1], 'Insertion'))

    return mutations

def save_to_csv_extended(mutations):
    """
    Bulunan mutasyonları bir CSV dosyasına kaydeder.

    Args:
        mutations (list): Mutasyon bilgilerini içeren liste.
    """
    with open("mutations_extended.csv", mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Pozisyon", "Orijinal", "Mutasyonlu", "Tür"])
        writer.writerows(mutations)
    print("\nGenişletilmiş mutasyonlar 'mutations_extended.csv' dosyasına kaydedildi.")

def plot_mutation_positions(mutations):
    """
    Mutasyonların pozisyonlarını ve türlerini bir nokta grafiği ile görselleştirir.

    Args:
        mutations (list): Mutasyon bilgilerini içeren liste.
    """
    df = pd.DataFrame(mutations, columns=['Pozisyon', 'Orijinal', 'Mutasyonlu', 'Tür'])
    colors = {'Replace': 'red', 'Deletion': 'blue', 'Insertion': 'green'}

    plt.figure(figsize=(10, 6))
    for mutation_type, group in df.groupby('Tür'):
        plt.scatter(group['Pozisyon'], [mutation_type] * len(group),
                    color=colors[mutation_type], label=mutation_type, s=100, alpha=0.7)

    plt.title("Mutasyon Pozisyonları ve Türleri", fontsize=14)
    plt.xlabel("Pozisyon", fontsize=12)
    plt.yticks(fontsize=10)
    plt.legend(title="Mutasyon Türleri", fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

def main():
    """
    Programın ana akışını yöneten işlev.
    Kullanıcıdan DNA dizilerini alır, mutasyon türlerini bulur, raporlar ve görselleştirir.
    """
    dna1, dna2 = get_dna_sequences()
    if check_length(dna1, dna2):
        mutations = align_and_identify_mutations(dna1, dna2)
    else:
        mutations = align_and_identify_mutations(dna1, dna2)

    save_to_csv_extended(mutations)

    # Kullanıcı grafik istiyorsa göster
    show_graph = input("Mutasyon pozisyonlarını grafik olarak görmek ister misiniz? (E/H): ").lower()
    if show_graph == 'e':
        plot_mutation_positions(mutations)

if __name__ == "__main__":
    main()
