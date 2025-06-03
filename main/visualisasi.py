import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Inisialisasi plot
fig, ax = plt.subplots(figsize=(6, 6))

# Warna area
colors = {
    'NT': '#4a90e2',       # biru
    'Minor': '#7ed957',    # hijau
    'Fallback': '#f45b69'  # merah
}

# Gambar kotak warna untuk setiap koordinat
for x in range(5):
    for y in range(5):
        if x >= 2 and y >= 2:
            label = 'NT'
        elif True:  # Asumsikan minor_fits selalu tersedia
            label = 'Minor'
        else:
            label = 'Fallback'

        # Tambahkan kotak dengan warna sesuai kategori
        rect = patches.Rectangle((x, y), 1, 1, linewidth=1, edgecolor='gray', 
                                 linestyle='--', facecolor=colors[label], alpha=0.8)
        ax.add_patch(rect)
        
        # Tambahkan teks label di tengah kotak
        ax.text(x + 0.5, y + 0.5, label, ha='center', va='center', fontsize=9, color='black')

# Set axis dan grid
ax.set_xlim(0, 5)
ax.set_ylim(0, 5)
ax.set_xticks(range(6))
ax.set_yticks(range(6))
ax.set_xticks([i + 0.5 for i in range(5)], minor=True)
ax.set_yticks([i + 0.5 for i in range(5)], minor=True)
ax.grid(which='minor', linestyle='--', color='gray', linewidth=0.5)
ax.set_xlabel('x_total (Spade stopper)')
ax.set_ylabel('y_total (Heart stopper)')
ax.set_title('Visualisasi Pembagian Area: NT, Minor Fit, Fallback')

plt.gca().set_aspect('equal', adjustable='box')
plt.tight_layout()
plt.show()

