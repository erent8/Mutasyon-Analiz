import csv
from difflib import SequenceMatcher
import matplotlib.pyplot as plt
import pandas as pd

# DNA dizilerini dosyadan ya da kullanıcıdan alma seçeneği
def get_dna_sequences():
    choice = input("DNA dizisini dosyadan mı yüklemek istersiniz? (E/H): ").lower()
    if choice == 'e':
        file_path = input("Dosya yolunu girin: ")
        with open(file_path, 'r') as file:
            lines = file.readlines()
            dna1 = lines[0].strip().upper()
            dna2 = lines[1].strip().upper()
    else:
        dna1 = input("Birinci DNA dizisini girin: ").upper()
        dna2 = input("İkinci DNA dizisini girin: ").upper()
    return dna1, dna2

# Uzunluk kontrolü
def check_length(dna1, dna2):
    if len(dna1) == len(dna2):
        print("\nDiziler aynı uzunlukta, baz bazına karşılaştırma yapılacak.\n")
        return True
    else:
        print("\nDiziler farklı uzunlukta, hizalama yapılacak.\n")
        return False

# Mutasyon bulma (aynı uzunluktaki diziler için)
def find_mutations(dna1, dna2):
    mutations = []
    for i in range(len(dna1)):
        if dna1[i] != dna2[i]:
            mutations.append((i + 1, dna1[i], dna2[i]))
    return mutations

# Farklı uzunlukta hizalama ve mutasyon bulma
def align_dna(dna1, dna2):
    matcher = SequenceMatcher(None, dna1, dna2)
    mutations = []
    for opcode in matcher.get_opcodes():
        tag, a0, a1, b0, b1 = opcode
        if tag == 'replace':
            mutations.append((a0 + 1, dna1[a0:a1], dna2[b0:b1]))
        elif tag == 'delete':
            mutations.append((a0 + 1, dna1[a0:a1], '-'))
        elif tag == 'insert':
            mutations.append((a0 + 1, '-', dna2[b0:b1]))
    return mutations

# Mutasyonları CSV dosyasına kaydetme
def save_to_csv(mutations):
    with open("mutations.csv", mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Pozisyon", "Orijinal", "Mutasyonlu"])
        writer.writerows(mutations)
    print("\nMutasyonlar 'mutations.csv' dosyasına kaydedildi.")

# Mutasyonları raporlama
def report_mutations(mutations):
    if not mutations:
        print("Hiçbir mutasyon tespit edilmedi.")
    else:
        print(f"Toplam {len(mutations)} mutasyon tespit edildi:")
        for mutation in mutations:
            print(f"Pozisyon {mutation[0]}: {mutation[1]} -> {mutation[2]}")
        
        save_to_csv(mutations)

# Mutasyonları grafik olarak gösterme
def plot_mutations(mutations):
    df = pd.DataFrame(mutations, columns=['Pozisyon', 'Orijinal', 'Mutasyonlu'])
    plt.bar(df['Pozisyon'], height=1)
    plt.title("Mutasyonların Pozisyonları")
    plt.xlabel("Pozisyon")
    plt.ylabel("Mutasyon Sayısı")
    plt.show()

# Ana fonksiyon
def main():
    dna1, dna2 = get_dna_sequences()
    if check_length(dna1, dna2):
        mutations = find_mutations(dna1, dna2)
    else:
        mutations = align_dna(dna1, dna2)
    
    report_mutations(mutations)
    
    # Kullanıcı grafik istiyorsa
    show_graph = input("Mutasyonları grafik olarak görmek ister misiniz? (E/H): ").lower()
    if show_graph == 'e':
        plot_mutations(mutations)

if __name__ == "__main__":

    main()
